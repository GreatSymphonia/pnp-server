#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#

# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2022-12-10
# File  : open-pnp.py

#
# Basic Cisco PnP server for Day0 provisioning
#

# Based on      : https://github.com/oliverl-21/Open-PnP-Server
# Cisco doc at  : https://developer.cisco.com/site/open-plug-n-play/learn/learn-open-pnp-protocol/
# TOML doc at   : https://toml.io/en/
# Jinja2 doc at : https://jinja.palletsprojects.com/en/3.0.x/templates/

# 2022-12-14: added count in status page
#             added check if image/config file is available
# 2022-12-15: renamed ./vars/vars.py to ./vars/settings.py
#             stop on import error for images.py and platforms.py
#             removed extending path variable to ./vars
# 2023-01-26: reorg platforms.py and images.py in images.json
#             reorg settings.py in open-pnp.ini
#             remove imports for platforms.py/images.py/settings.py
#             added reload data function
#             changed open-pnp.ini/images.json to open-pnp.toml/images.toml for better handling
# 2023-01-27: added default IOS/IOS-XE config file fallback
# 2023-01-28: moved global variables to Settings class
#             integrated status_debug.html with status.html
# 2023-01-29: rework of status page, make table body scrollable
# 2023-02-01: added cli options, changed debug/log output
#             cleanup: removed global variables
# 2023-02-22: removed regex -> was not working with PID: ISR4451-X/K9
#             added PNP_SERVER_VERSION
# 2023-02-23: added cli option -v/--version, --default_cfg
# 2023-02-26: reorganized open-pnp.py in to open_pnp_classes.py and open_pnp_utils.py
# 2023-32-07: changed '_' in cli options to '-' -> better readable/more bash like
# 2023-03-13: added '--no-default-cfg' option
# 2023-04-11: added flask options to remove whitespaces by default, changed version format (major.minor.micro-date)
# 2023-04-17: fixed device update check use version instead of image
#
# pip install flask xmltodict requests ifaddr tomli
#

# ToDo:
#       add "install remove inactive" images job on IOS-XE devices if no space for image update

# system libs
# from re import compile as re_compile
from csv import DictReader
from json import dump as json_dump, load as json_load
from os import makedirs, replace
from os.path import dirname, isfile, join
from re import search
from time import strftime
from typing import Optional, Dict, Any
from requests import head
from logging import getLogger
from unicodedata import normalize
from urllib.parse import urlencode

# additional libs
from flask import (
    Flask, 
    Response,
    send_from_directory, 
    render_template, 
    redirect, 
    request,
    cli
)
from xmltodict import parse as xml_parse

from open_pnp_classes import (
    Device,
    SoftwareImage,
    ErrorCodes,
    PnpFlow,
    Settings,
    Images
)

from open_pnp_utils import (
    configure_logger,
    log_info,
    parse_arguments,
    get_local_ip_addresses,
)


PNP_SERVER_VERSION = '1.0.4-202300411'


def normalize_text(value: str) -> str:
    if not value:
        return ''
    normalized = normalize('NFKD', value)
    return ''.join(c for c in normalized if ord(c) < 128).strip().lower()


def load_hostname_mapping(mapping_file: str) -> Dict[str, str]:
    if not mapping_file or not isfile(mapping_file):
        if mapping_file:
            print(f'WARNING: Mapping file {mapping_file} not found')
        return {}

    mapping: Dict[str, str] = {}
    serial_candidates = ['serial', 'no serie', 'no serie', 'sn', 'boardid', 'board id']
    hostname_candidates = ['hostname', 'identifiant', 'name', 'switch']

    with open(mapping_file, mode='r', encoding='utf-8-sig', newline='') as file_handle:
        reader = DictReader(file_handle, delimiter=';')
        if not reader.fieldnames:
            return mapping

        normalized_headers = {
            normalize_text(header): header
            for header in reader.fieldnames
            if header
        }

        serial_key = ''
        hostname_key = ''

        for candidate in serial_candidates:
            if candidate in normalized_headers:
                serial_key = normalized_headers[candidate]
                break

        for candidate in hostname_candidates:
            if candidate in normalized_headers:
                hostname_key = normalized_headers[candidate]
                break

        if not serial_key or not hostname_key:
            print(
                f'WARNING: Could not detect serial/hostname columns in mapping file {mapping_file}. '
                'Expected columns like "No Série" and "Identifiant".'
            )
            return mapping

        for row in reader:
            serial = str(row.get(serial_key, '')).strip().upper()
            hostname = str(row.get(hostname_key, '')).strip()
            if serial and hostname:
                mapping[serial] = hostname

    return mapping


def hostname_from_config(serial: str) -> str:
    if not serial:
        return ''

    cfg_file = join('configs', f'{serial}.cfg')
    if not isfile(cfg_file):
        return ''

    try:
        with open(cfg_file, mode='r', encoding='utf-8', errors='ignore') as file_handle:
            for line in file_handle:
                match = search(r'^\s*hostname\s+(\S+)\s*$', line, flags=0)
                if match:
                    return match.group(1)
    except OSError:
        return ''

    return ''


def resolve_device_hostname(device: Device):
    serial = device.serial.strip().upper()
    if not serial:
        device.hostname = ''
        return

    if serial in HOSTNAME_MAP:
        device.hostname = HOSTNAME_MAP[serial]
    elif not device.hostname and SETTINGS.hostname_from_config:
        device.hostname = hostname_from_config(serial)


def assign_target_image(device: Device):
    if device.target_image:
        return

    for image, image_data in IMAGES.images.items():
        if device.platform in image_data['models']:
            device.target_image = SoftwareImage(
                image=image,
                version=image_data['version'],
                md5=image_data['md5'],
                size=image_data['size'],
            )
            return


def software_image_to_dict(image: Optional[SoftwareImage]) -> Dict[str, Any]:
    if image is None:
        return {}
    return {
        'image': image.image,
        'version': image.version,
        'md5': image.md5,
        'size': image.size,
    }


def device_to_dict(device: Device) -> Dict[str, Any]:
    return {
        'udi': device.udi,
        'platform': device.platform,
        'hw_rev': device.hw_rev,
        'serial': device.serial,
        'hostname': device.hostname,
        'ip_address': device.ip_address,
        'current_job': device.current_job,
        'first_seen': device.first_seen,
        'last_contact': device.last_contact,
        'version': device.version,
        'image': device.image,
        'destination_name': device.destination_name,
        'destination_free': device.destination_free,
        'status': device.status,
        'pnp_flow': device.pnp_flow,
        'target_image': software_image_to_dict(device.target_image),
        'backoff': device.backoff,
        'refresh_data': device.refresh_data,
        'error_code': device.error_code,
        'error_count': device.error_count,
        'error_message': device.error_message,
        'hard_error': device.hard_error,
        'status_class': device.status_class,
    }


def device_from_dict(data: Dict[str, Any]) -> Optional[Device]:
    try:
        device = Device(
            udi=str(data.get('udi', '')),
            platform=str(data.get('platform', '')),
            hw_rev=str(data.get('hw_rev', '')),
            serial=str(data.get('serial', '')),
            first_seen=str(data.get('first_seen', strftime(SETTINGS.time_format))),
            last_contact=str(data.get('last_contact', strftime(SETTINGS.time_format))),
            src_address=str(data.get('ip_address', '')),
            current_job=str(data.get('current_job', 'urn:cisco:pnp:device-info')),
        )
    except (KeyError, TypeError, ValueError):
        return None

    device.hostname = str(data.get('hostname', ''))
    device.version = str(data.get('version', ''))
    device.image = str(data.get('image', ''))
    device.destination_name = str(data.get('destination_name', ''))
    device.destination_free = data.get('destination_free')
    device.status = str(data.get('status', ''))

    target_image = data.get('target_image', {}) or {}
    if target_image and target_image.get('image'):
        device.target_image = SoftwareImage(
            image=str(target_image.get('image', '')),
            version=str(target_image.get('version', '')),
            md5=str(target_image.get('md5', '')),
            size=int(target_image.get('size', 0)),
        )
    else:
        assign_target_image(device)

    device.pnp_flow = int(data.get('pnp_flow', PNPFLOW.NEW))
    device.backoff = bool(data.get('backoff', False))
    device.refresh_data = bool(data.get('refresh_data', False))
    device.error_count = int(data.get('error_count', 0))
    device.error_message = str(data.get('error_message', ''))

    error_code = int(data.get('error_code', ERROR.ERROR_NO_ERROR))
    if error_code != ERROR.ERROR_NO_ERROR:
        device.error_code = error_code

    if bool(data.get('hard_error', False)):
        device.hard_error = True

    status_class = str(data.get('status_class', ''))
    if status_class:
        device.status_class = status_class

    resolve_device_hostname(device)
    return device


def save_device_state():
    state_file = SETTINGS.state_file
    if not state_file:
        return

    base_dir = dirname(state_file)
    if base_dir:
        makedirs(base_dir, exist_ok=True)

    payload = {
        'version': PNP_SERVER_VERSION,
        'devices': [device_to_dict(device) for device in devices.values()],
    }

    tmp_file = f'{state_file}.tmp'
    try:
        with open(tmp_file, mode='w', encoding='utf-8') as file_handle:
            json_dump(payload, file_handle, ensure_ascii=True, indent=2)
        replace(tmp_file, state_file)
    except OSError as exc:
        print(f'WARNING: Could not save device state to {state_file} ({exc})')


def load_device_state():
    state_file = SETTINGS.state_file
    if not state_file or not isfile(state_file):
        return

    try:
        with open(state_file, mode='r', encoding='utf-8') as file_handle:
            payload = json_load(file_handle)
    except (OSError, ValueError) as exc:
        print(f'WARNING: Could not load device state from {state_file} ({exc})')
        return

    loaded_devices = payload.get('devices', []) if isinstance(payload, dict) else []
    restored = 0
    for entry in loaded_devices:
        if not isinstance(entry, dict):
            continue
        device = device_from_dict(entry)
        if not device:
            continue
        devices[device.udi] = device
        restored += 1

    if restored:
        print(f'Restored {restored} device(s) from state file {state_file}')


def filter_devices(device_list, filter_text: str, filter_field: str):
    allowed_fields = {'all', 'hostname', 'serial', 'platform', 'ip_address', 'status'}
    active_field = filter_field if filter_field in allowed_fields else 'all'
    search_text = (filter_text or '').strip().lower()

    if not search_text:
        return device_list, active_field, ''

    def _matches(device: Device):
        candidates = {
            'hostname': str(getattr(device, 'hostname', '') or '').lower(),
            'serial': str(getattr(device, 'serial', '') or '').lower(),
            'platform': str(getattr(device, 'platform', '') or '').lower(),
            'ip_address': str(getattr(device, 'ip_address', '') or '').lower(),
            'status': str(getattr(device, 'status', '') or '').lower(),
        }

        if active_field == 'all':
            return any(search_text in value for value in candidates.values())

        return search_text in candidates[active_field]

    filtered = [device for device in device_list if _matches(device)]
    return filtered, active_field, filter_text


def sorted_devices(device_dict: Dict[str, Device], sort_by: str, sort_order: str, filter_text: str, filter_field: str):
    allowed_sort = {
        'hostname', 'serial', 'platform', 'ip_address',
        'pnp_flow', 'status', 'first_seen', 'last_contact'
    }
    key_name = sort_by if sort_by in allowed_sort else 'last_contact'
    reverse = sort_order == 'desc'

    device_list = list(device_dict.values())

    for device in device_list:
        resolve_device_hostname(device)

    def _sort_value(device: Device):
        if key_name == 'pnp_flow':
            return getattr(device, 'pnp_flow', 0)
        value = getattr(device, key_name, '')
        if value is None:
            return ''
        return str(value).lower()

    filtered_device_list, active_filter_field, active_filter_text = filter_devices(
        device_list, filter_text, filter_field
    )

    filtered_device_list.sort(key=_sort_value, reverse=reverse)
    return filtered_device_list, key_name, ('desc' if reverse else 'asc'), active_filter_field, active_filter_text


def pnp_device_info(udi: str, correlator: str, info_type: str) -> str:
    # info_type can be one of:
    # image, hardware, filesystem, udi, profile, all
    device = devices[udi]
    if device.current_job != 'urn:cisco:pnp:image-install':
        device.current_job = 'urn:cisco:pnp:device-info'
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
        'info_type': info_type
    }
    _template = render_template('device_info.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


def pnp_backoff(udi: str, correlator: str, minutes: Optional[int] = 1) -> str:
    seconds = 0
    hours = 0
    device = devices[udi]
    device.status = f'backoff for {hours:02d}:{minutes:02d}:{seconds:02d}'
    device.current_job = 'urn:cisco:pnp:backoff'
    device.backoff = False
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
        'seconds': seconds,
        'minutes': minutes,
        'hours': hours,
    }
    _template = render_template('backoff.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


# will not be used as we remove PNP via EEM. PNP terminate is missing a "write mem"
def pnp_backoff_terminate(udi: str, correlator: str) -> str:
    device = devices[udi]
    # device.status_class = f'finished'
    device.pnp_flow = PNPFLOW.FINISHED
    device.current_job = 'urn:cisco:pnp:backoff-terminate'
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
    }
    _template = render_template('backoff_terminate.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


def pnp_install_image(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    response = head(f'{SETTINGS.image_url}/{device.target_image.image}')
    if response.status_code == 200:
        device.current_job = 'urn:cisco:pnp:image-install'
        device.pnp_flow = PNPFLOW.UPDATE_START
        device.backoff = True
        device.refresh_data = True
        jinja_context = {
            'udi': udi,
            'correlator': correlator,
            'base_url': SETTINGS.image_url,
            'image': device.target_image.image,
            'md5': device.target_image.md5.lower(),
            'destination': device.destination_name,
            'delay': 0,  # reload in seconds
        }
        _template = render_template('image_install.xml', **jinja_context)
        log_info(_template, SETTINGS.debug)
        return _template
    else:
        device.error_code = ERROR.ERROR_NO_IMAGE_FILE
        device.hard_error = True


def pnp_config_upgrade(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    cfg_file = f'{device.serial}.cfg'
    response = head(f'{SETTINGS.config_url}/{cfg_file}')
    if response.status_code != 200:  # SERIAL.cfg not found
        if not SETTINGS.no_default_cfg:
            cfg_file = SETTINGS.default_cfg
            response = head(f'{SETTINGS.config_url}/{cfg_file}')
            if response.status_code != 200:  # DEFAULT.cfg also not found
                device.error_code = ERROR.ERROR_NO_CFG_FILE
                device.hard_error = True
                return
        else:
            device.error_code = ERROR.ERROR_NO_CFG_FILE
            device.hard_error = True
            return

    device.current_job = 'urn:cisco:pnp:device-info'
    device.pnp_flow = PNPFLOW.CONFIG_START
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
        'base_url': SETTINGS.config_url,
        'reload_delay': 30,  # reload in seconds
        'cfg_file': cfg_file,
    }
    _template = render_template('config_upgrade.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


def pnp_remove_inactive(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    cfg_file = 'REMOVE_INACTIVE.cfg'
    response = head(f'{SETTINGS.config_url}/{cfg_file}')
    if response.status_code != 200:  # cfg not found
        device.error_code = ERROR.ERROR_NO_CFG_FILE
        device.hard_error = True
        return

    device.current_job = 'urn:cisco:pnp:config-upgrade'
    device.pnp_flow = PNPFLOW.CLEANUP_START
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
        'base_url': SETTINGS.config_url,
        'cfg_file': cfg_file,
    }
    _template = render_template('config_upgrade.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


def pnp_bye(udi: str, correlator: str) -> str:
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
    }
    _template = render_template('bye.xml', **jinja_context)
    log_info(_template, SETTINGS.debug)
    return _template


def create_new_device(udi: str, src_add: str):
    # sample udi: PID:ISR4451-X/K9,VID:V08,SN:FCZ230640AB
    # serial_num_re = re_compile(r'PID:(?P<product_id>[\w\/]+(?:-\w+)*),'
    #                            r'VID:(?P<hw_version>\w+),SN:(?P<serial_number>\w+)')
    # platform, hw_rev, serial = serial_num_re.findall(udi)[0]

    _udi = udi.split(',')
    platform = _udi[0].split(':')[1]
    hw_rev = _udi[1].split(':')[1]
    serial = _udi[2].split(':')[1]

    devices[udi] = Device(
        udi=udi,
        first_seen=strftime(SETTINGS.time_format),
        last_contact=strftime(SETTINGS.time_format),
        src_address=src_add,
        serial=serial,
        platform=platform,
        hw_rev=hw_rev,
        current_job='urn:cisco:pnp:device-info',
    )
    device = devices[udi]
    resolve_device_hostname(device)
    device.backoff = True
    assign_target_image(device)
    if not device.target_image:
        device.error_code = ERROR.ERROR_NO_PLATFORM
        device.hard_error = True
    save_device_state()


def update_device_info(data: Dict[str, Any]):
    destination = {}

    udi = data['pnp']['@udi']
    device = devices[udi]

    device.version = data['pnp']['response']['imageInfo']['versionString'].strip()
    device.image = data['pnp']['response']['imageInfo']['imageFile'].split(':')[1]
    device.refresh_data = False
    device.last_contact = strftime(SETTINGS.time_format)
    for filesystem in data['pnp']['response']['fileSystemList']['fileSystem']:
        if filesystem['@name'] in ['bootflash', 'flash']:
            destination = filesystem

    device.platform = data['pnp']['response']['hardwareInfo']['platformName']
    device.serial = data['pnp']['response']['hardwareInfo']['boardId']
    resolve_device_hostname(device)
    assign_target_image(device)
    device.destination_name = destination['@name']
    device.destination_free = int(destination['@freespace'])
    save_device_state()


def check_update(udi: str):
    device = devices[udi]
    if device.version == device.target_image.version:
        device.pnp_flow = PNPFLOW.UPDATE_DOWN
    else:
        device.pnp_flow = PNPFLOW.UPDATE_NEEDED
        if device.destination_free < device.target_image.size:
            _mb = round(device.target_image.size / 1024 / 1024)
            device.error_code = ERROR.ERROR_NO_FREE_SPACE
            device.hard_error = True


# flask
app = Flask(__name__, template_folder='./templates')
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True  # removes empty lines, i.e. in loops


@app.route('/')
def root():
    return redirect('/status', 302)


@app.route('/status', methods=['GET'])
def status():
    sort_by = request.args.get('sort_by', 'last_contact')
    sort_order = request.args.get('sort_order', 'desc')
    filter_text = request.args.get('filter_text', '')
    filter_field = request.args.get('filter_field', 'all')
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'

    device_list, active_sort_by, active_sort_order, active_filter_field, active_filter_text = sorted_devices(
        devices,
        sort_by,
        sort_order,
        filter_text,
        filter_field,
    )

    jinja_context = {
        'devices': device_list,
        'refresh': SETTINGS.status_refresh,
        'config_url': SETTINGS.config_url,
        'image_url': SETTINGS.image_url,
        'debug': SETTINGS.debug,
        'sort_by': active_sort_by,
        'sort_order': active_sort_order,
        'filter_field': active_filter_field,
        'filter_text': active_filter_text,
        'pnp_server_version': PNP_SERVER_VERSION,
    }
    result = render_template('status.html', **jinja_context)
    return Response(result)


@app.route('/buttons', methods=['POST'])
def buttons():
    udi = ''
    button = ''

    if 'reload_data' in request.form:
        button = 'Reload CFG'
    else:
        for key, value in request.form.items():
            if key in ['sort_by', 'sort_order', 'filter_field', 'filter_text']:
                continue
            if value in ['Remove', 'Refresh']:
                udi = key
                button = value
                break

        if button == '':
            udi = list(request.form.keys())[0]
            button = list(request.form.values())[0]
    sort_by = request.form.get('sort_by', request.args.get('sort_by', 'last_contact'))
    sort_order = request.form.get('sort_order', request.args.get('sort_order', 'desc'))
    filter_field = request.form.get('filter_field', request.args.get('filter_field', 'all'))
    filter_text = request.form.get('filter_text', request.args.get('filter_text', ''))

    if button == 'Reload CFG':
        IMAGES.load_image_data(SETTINGS.image_data)
        SETTINGS.update(SETTINGS.config_file)
        HOSTNAME_MAP.clear()
        HOSTNAME_MAP.update(load_hostname_mapping(SETTINGS.mapping_file))
        for _device in devices.values():
            resolve_device_hostname(_device)

    if udi in devices.keys():
        device = devices[udi]
        if button == "Remove":
            devices.pop(udi)
        elif button == 'Refresh':
            device.refresh_data = True
            device.error_message = ''

    save_device_state()

    query = urlencode({
        'sort_by': sort_by,
        'sort_order': sort_order,
        'filter_field': filter_field,
        'filter_text': filter_text,
    })
    return redirect(f'/status?{query}', 302)


@app.route('/configs/<path:file>')
def serve_configs(file):
    return send_from_directory('configs', file, mimetype='text/plain')


@app.route('/images/<path:file>')
def serve_sw_images(file):
    return send_from_directory('images', file, mimetype='application/octet-stream')


@app.route('/pnp/HELLO')
def pnp_hello():
    return '', 200


@app.route('/pnp/WORK-REQUEST', methods=['POST'])
def pnp_work_request():
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    data = xml_parse(request.data)
    log_info(f'REQUEST: {data}', SETTINGS.debug)
    correlator = data['pnp']['info']['@correlator']
    udi = data['pnp']['@udi']
    if udi in devices.keys():
        device = devices[udi]
        device.last_contact = strftime(SETTINGS.time_format)
        device.ip_address = src_add
        if device.hard_error:
            response = Response(pnp_backoff(udi, correlator, 10), mimetype='text/xml')
            save_device_state()
            return response
            pass
        if device.backoff:
            log_info('BACKOFF', SETTINGS.debug)
            # backoff more and more on errors, max error_count = 11 -> 5 * 11 = 55
            # error_count == 12 -> like hard_error
            minutes = device.error_count + 1
            if minutes > 10:
                device.hard_error = True
            response = Response(pnp_backoff(udi, correlator, minutes), mimetype='text/xml')
            save_device_state()
            return response
        if device.pnp_flow == PNPFLOW.NEW:
            log_info('PNPFLOW.NEW', SETTINGS.debug)
            device.pnp_flow = PNPFLOW.INFO
            response = Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
            save_device_state()
            return response
        if device.pnp_flow == PNPFLOW.UPDATE_NEEDED:
            log_info('PNPFLOW.UPDATE_NEEDED', SETTINGS.debug)
            device.pnp_flow = PNPFLOW.UPDATE_START
            response = Response(pnp_install_image(udi, correlator), mimetype='text/xml')
            save_device_state()
            return response
        if device.pnp_flow == PNPFLOW.UPDATE_RELOAD:
            log_info('PNPFLOW.UPDATE_RELOAD', SETTINGS.debug)
            response = Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
            save_device_state()
            return response
        if device.pnp_flow == PNPFLOW.UPDATE_DOWN:
            log_info('PNPFLOW.UPDATE_DOWN', SETTINGS.debug)
            response = Response(pnp_config_upgrade(udi, correlator), mimetype='text/xml')
            save_device_state()
            return response
        if device.pnp_flow == PNPFLOW.CONFIG_DOWN:  # will never reach this point, as pnp is removed bei EEM :-)
            log_info('PNPFLOW.CONFIG_DOWN', SETTINGS.debug)
            response = Response(pnp_backoff_terminate(udi, correlator), mimetype='text/xml')
            save_device_state()
            return response
        log_info(
            f'Other PNP_FLOW: {PNPFLOW.readable(device.pnp_flow)}', SETTINGS.debug)
        response = Response('', 200)
        save_device_state()
        return response
    else:
        log_info('REQUEST NEW DEVICE FOUND', SETTINGS.debug)
        create_new_device(udi, src_add)
        # return Response(device_info(udi, correlator, 'all'), mimetype='text/xml')
        devices[udi].pnp_flow = PNPFLOW.NEW
        response = Response(pnp_backoff(udi, correlator), mimetype='text/xml')
        save_device_state()
        return response
        # return Response('', 200)


@app.route('/pnp/WORK-RESPONSE', methods=['POST'])
def pnp_work_response():
    data = xml_parse(request.data)
    log_info(f'RESPONSE: {data}', SETTINGS.debug)
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    udi = data['pnp']['@udi']
    job_type = data['pnp']['response']['@xmlns']
    if udi not in devices.keys():
        create_new_device(udi, src_add)

    device = devices[udi]
    device.ip_address = src_add
    device.last_contact = strftime(SETTINGS.time_format)

    if job_type == 'urn:cisco:pnp:fault':  # error without job info (correlator):-(
        device.error_message = data['pnp']['response']['fault']['detail']['XSVC-ERR:error']['XSVC-ERR:details']
        save_device_state()
    else:
        correlator = data['pnp']['response']['@correlator']
        job_status = int(data['pnp']['response']['@success'])
        log_info(f'Correlator: {correlator}', SETTINGS.debug)
        log_info(f'Job type: {job_type}', SETTINGS.debug)
        log_info(f'PnP flow: {device.pnp_flow_readable}', SETTINGS.debug)
        log_info(f'Job status: {job_status}', SETTINGS.debug)
        if job_status == 1:  # success
            if job_type not in ['urn:cisco:pnp:backoff']:
                device.backoff = True
            device.error_count = 0
            if job_type == 'urn:cisco:pnp:device-info':
                if device.pnp_flow in [PNPFLOW.INFO, PNPFLOW.UPDATE_RELOAD]:
                    update_device_info(data)
                    check_update(udi)
                else:
                    update_device_info(data)
            elif job_type == 'urn:cisco:pnp:image-install':
                device.pnp_flow = PNPFLOW.UPDATE_RELOAD
            elif job_type == 'urn:cisco:pnp:config-upgrade':
                # device.pnp_flow = PNPFLOW.CONFIG_DOWN  # we don't reach this as we remove PNP before via EEM
                device.pnp_flow = PNPFLOW.FINISHED
                device.status = 'Finished. You can remove the device from the list :-)'
            elif job_type == 'urn:cisco:pnp:backoff':
                # device.pnp_flow = PNPFLOW.INFO
                pass
            _response = pnp_bye(udi, correlator)
            log_info(_response, SETTINGS.debug)
            save_device_state()
            return Response(_response, mimetype='text/xml')
        elif job_status == 0:
            error_code = int(data['pnp']['response']['errorInfo']['errorCode'].split(' ')[-1])
            device.error_count += 1
            device.error_message = data['pnp']['response']['errorInfo']['errorMessage']
            device.error_code = error_code
            if error_code in [ERROR.PNP_ERROR_BAD_CHECKSUM, ERROR.PNP_ERROR_FILE_NOT_FOUND]:
                device.hard_error = True
            save_device_state()
            return Response(pnp_bye(udi, correlator), mimetype='text/xml')
    device.current_job = 'none'
    log_info('Empty Response', SETTINGS.debug)
    save_device_state()
    return Response('')


if __name__ == '__main__':
    # clear screen
    print("\033c\033[3J", end='')

    ERROR = ErrorCodes()
    PNPFLOW = PnpFlow()
    SETTINGS = Settings(vars(parse_arguments(PNP_SERVER_VERSION)))
    # SETTINGS.update(SETTINGS.cfg_file)

    if SETTINGS.version:
        print(PNP_SERVER_VERSION)
        exit(0)

    IMAGES = Images(SETTINGS.image_data)
    HOSTNAME_MAP = load_hostname_mapping(SETTINGS.mapping_file)

    devices: Dict[str, Device] = {}
    load_device_state()

    if SETTINGS.debug:
        app.debug = True
    else:
        # disable FLASK console output
        getLogger("werkzeug").disabled = True
        cli.show_server_banner = lambda *args: None

    if SETTINGS.image_url == '':
        print(f'image-url not set, check {SETTINGS.config_file} or see open-pnp.py -h')
        exit(1)
    if SETTINGS.config_url == '':
        print(f'config-url not set, check {SETTINGS.config_file} or see open-pnp.py -h')
        exit(1)

    if SETTINGS.debug:
        configure_logger(SETTINGS.log_file, SETTINGS.log_to_console)
        log_info('STARTED LOGGER', SETTINGS.debug)

    print()
    print(f'Running open PnP server. Stop with ctrl+c')
    print()
    print(f'Bind to IP-address      : {SETTINGS.bind_pnp_server}')
    print(f'Listen on port          : {SETTINGS.port}')
    print(f'Image file(s) base URL  : {SETTINGS.image_url}')
    print(f'Config file(s) base URL : {SETTINGS.config_url}')
    print()
    print('The PnP server is running on the following URL(s)')
    if SETTINGS.bind_pnp_server in ['0.0.0.0', '::']:
        addresses = get_local_ip_addresses()
        for address in addresses:
            print(f'    http://{address}:{SETTINGS.port}')
    else:
        print(f'Status page running on : http://{SETTINGS.bind_pnp_server}:{SETTINGS.port}')
    print()
    print(f'{PNP_SERVER_VERSION} | '
          f'Written by thl-cmk[at]outlook[dot]com | '
          f'see https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision')
    print()
    app.run(host=SETTINGS.bind_pnp_server, port=SETTINGS.port)
