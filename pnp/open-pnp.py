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
# based on https://github.com/oliverl-21/Open-PnP-Server
#
# Cisco doc on https://developer.cisco.com/site/open-plug-n-play/learn/learn-open-pnp-protocol/
#
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
#
# pip install flask xmltodict requests ifaddr tomli
#
# ToDo:
#       add remove inactive job on IOS-XE devices if no space for image update

# system libs
# from re import compile as re_compile
from time import strftime
from typing import Optional, Dict, Any
from requests import head
from logging import getLogger

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


PNP_SERVER_VERSION = '20230313.v1.0.3'


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
    device.backoff = True
    for image, image_data in IMAGES.images.items():
        if platform in image_data['models']:
            device.target_image = SoftwareImage(
                image=image,
                version=image_data['version'],
                md5=image_data['md5'],
                size=image_data['size']
            )
    if not device.target_image:
        device.error_code = ERROR.ERROR_NO_PLATFORM
        device.hard_error = True


def update_device_info(data: Dict[str, Any]):
    destination = {}

    udi = data['pnp']['@udi']
    device = devices[udi]

    device.version = data['pnp']['response']['imageInfo']['versionString']
    device.image = data['pnp']['response']['imageInfo']['imageFile'].split(':')[1]
    device.refresh_data = False
    device.last_contact = strftime(SETTINGS.time_format)
    for filesystem in data['pnp']['response']['fileSystemList']['fileSystem']:
        if filesystem['@name'] in ['bootflash', 'flash']:
            destination = filesystem

    device.platform = data['pnp']['response']['hardwareInfo']['platformName']
    device.serial = data['pnp']['response']['hardwareInfo']['boardId']
    device.destination_name = destination['@name']
    device.destination_free = int(destination['@freespace'])


def check_update(udi: str):
    device = devices[udi]
    if device.image == device.target_image.image:
        device.pnp_flow = PNPFLOW.UPDATE_DOWN
    else:
        device.pnp_flow = PNPFLOW.UPDATE_NEEDED
        if device.destination_free < device.target_image.size:
            _mb = round(device.target_image.size / 1024 / 1024)
            device.error_code = ERROR.ERROR_NO_FREE_SPACE
            device.hard_error = True


# flask
app = Flask(__name__, template_folder='./templates')


@app.route('/')
def root():
    return redirect('/status', 302)


@app.route('/status', methods=['GET'])
def status():
    device_list = []
    for device in devices.values():
        device_list.append(device)
    jinja_context = {
        'devices': device_list,
        'refresh': SETTINGS.status_refresh,
        'config_url': SETTINGS.config_url,
        'image_url': SETTINGS.image_url,
        'debug': SETTINGS.debug,
        'pnp_server_version': PNP_SERVER_VERSION,
    }
    result = render_template('status.html', **jinja_context)
    return Response(result)


@app.route('/buttons', methods=['POST'])
def buttons():
    udi = list(request.form.keys())[0]
    button = list(request.form.values())[0]

    if button == 'Reload CFG':
        IMAGES.load_image_data(SETTINGS.image_data)
        SETTINGS.update(SETTINGS.cfg_file)

    if udi in devices.keys():
        device = devices[udi]
        if button == "Remove":
            devices.pop(udi)
        elif button == 'Refresh':
            device.refresh_data = True
            device.error_message = ''

    return redirect('/status', 302)


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
            return Response(pnp_backoff(udi, correlator, 10), mimetype='text/xml')
            pass
        if device.backoff:
            log_info('BACKOFF', SETTINGS.debug)
            # backoff more and more on errors, max error_count = 11 -> 5 * 11 = 55
            # error_count == 12 -> like hard_error
            minutes = device.error_count + 1
            if minutes > 10:
                device.hard_error = True
            return Response(pnp_backoff(udi, correlator, minutes), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.NEW:
            log_info('PNPFLOW.NEW', SETTINGS.debug)
            device.pnp_flow = PNPFLOW.INFO
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_NEEDED:
            log_info('PNPFLOW.UPDATE_NEEDED', SETTINGS.debug)
            device.pnp_flow = PNPFLOW.UPDATE_START
            return Response(pnp_install_image(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_RELOAD:
            log_info('PNPFLOW.UPDATE_RELOAD', SETTINGS.debug)
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_DOWN:
            log_info('PNPFLOW.UPDATE_DOWN', SETTINGS.debug)
            return Response(pnp_config_upgrade(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.CONFIG_DOWN:  # will never reach this point, as pnp is removed bei EEM :-)
            log_info('PNPFLOW.CONFIG_DOWN', SETTINGS.debug)
            return Response(pnp_backoff_terminate(udi, correlator), mimetype='text/xml')
        log_info(
            f'Other PNP_FLOW: {PNPFLOW.readable(device.pnp_flow)}', SETTINGS.debug)
        return Response('', 200)
    else:
        log_info('REQUEST NEW DEVICE FOUND', SETTINGS.debug)
        create_new_device(udi, src_add)
        # return Response(device_info(udi, correlator, 'all'), mimetype='text/xml')
        devices[udi].pnp_flow = PNPFLOW.NEW
        return Response(pnp_backoff(udi, correlator), mimetype='text/xml')
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
        device.error = data['pnp']['response']['fault']['detail']['XSVC-ERR:error']['XSVC-ERR:details']
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
            return Response(_response, mimetype='text/xml')
        elif job_status == 0:
            error_code = int(data['pnp']['response']['errorInfo']['errorCode'].split(' ')[-1])
            device.error_count += 1
            device.error_message = data['pnp']['response']['errorInfo']['errorMessage']
            device.error_code = error_code
            if error_code in [ERROR.PNP_ERROR_BAD_CHECKSUM, ERROR.PNP_ERROR_FILE_NOT_FOUND]:
                device.hard_error = True
            return Response(pnp_bye(udi, correlator), mimetype='text/xml')
    device.current_job = 'none'
    log_info('Empty Response', SETTINGS.debug)
    return Response('')


if __name__ == '__main__':

    ERROR = ErrorCodes()
    PNPFLOW = PnpFlow()
    SETTINGS = Settings(vars(parse_arguments(PNP_SERVER_VERSION)))
    SETTINGS.update(SETTINGS.cfg_file)

    if SETTINGS.version:
        print(PNP_SERVER_VERSION)
        exit(0)

    IMAGES = Images(SETTINGS.image_data)

    devices: Dict[str, Device] = {}

    if SETTINGS.debug:
        app.debug = True
    else:
        # disable FLASK console output
        getLogger("werkzeug").disabled = True
        cli.show_server_banner = lambda *args: None

    if SETTINGS.image_url == '':
        print(f'image-url not set, check {SETTINGS.cfg_file} or see open-pnp.py -h')
        exit(1)
    if SETTINGS.config_url == '':
        print(f'config-url not set, check {SETTINGS.cfg_file} or see open-pnp.py -h')
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
          f'Written by thl-cmk, see https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision')
    print()
    app.run(host=SETTINGS.bind_pnp_server, port=SETTINGS.port)
