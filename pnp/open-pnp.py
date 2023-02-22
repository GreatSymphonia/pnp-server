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
#
# pip install flask xmltodict requests ifaddr tomli
#

# system libs
import logging
from logging.handlers import RotatingFileHandler
# from re import compile as re_compile
from time import strftime
from typing import Optional, List, Dict, Any
from requests import head
from sys import stdout
from argparse import (
    Namespace as arg_Namespace,
    ArgumentParser,
    RawTextHelpFormatter,
)

# additional libs
from flask import Flask, request, send_from_directory, render_template, Response, redirect, cli
from xmltodict import parse as xml_parse
from ifaddr import get_adapters
from tomli import load as toml_load
from tomli import TOMLDecodeError

PNP_SERVER_VERSION = '20230222.v1.0.0'


class Settings:
    def __init__(
            self,
            cli_args: Dict[str, any],
            cfg_file: Optional[str] = 'open-pnp.toml',
            image_data: Optional[str] = 'images.toml',
            bind_pnp_server: Optional[str] = '0.0.0.0',
            port: Optional[int] = 8080,
            time_format: Optional[str] = '%Y-%m-%dT%H:%M:%S',
            status_refresh: Optional[int] = 60,
            debug: Optional[bool] = False,
            log_to_console: Optional[bool] = False,
            log_file: Optional[str] = 'log/pnp_debug.log',
            image_url: Optional[str] = '',
            config_url: Optional[str] = '',
            default_cfg_file: Optional[str] = 'DEFAULT.cfg',
    ):
        self.__settings = {
            'cfg_file': cfg_file,
            'image_data': image_data,
            'bind_pnp_server': bind_pnp_server,
            'port': port,
            'time_format': time_format,
            'status_refresh': status_refresh,
            'debug': debug,
            'log_to_console': log_to_console,
            'log_file': log_file,
            'image_url': image_url,
            'config_url': config_url,
            'default_cfg_file': default_cfg_file,
        }
        self.__args = {}
        self.__set_cli_args(cli_args)

    def __set_cli_args(self, cli_args: Dict[str, any]):
        self.__args = ({k: v for k, v in cli_args.items() if v})
        self.__settings.update(self.__args)

    def update(self, cfg_file: str):
        try:
            with open(cfg_file, 'rb') as f:
                self.__settings.update(toml_load(f))
        except FileNotFoundError as e:
            print(f'ERROR: Data file {cfg_file} not found! ({e})')
            exit(1)
        except TOMLDecodeError as e:
            print(f'ERROR: Data file {cfg_file} is not in valid toml format! ({e})')
            exit(2)

        self.__settings.update(self.__args)

    @property
    def cfg_file(self) -> str:
        return self.__settings['cfg_file']

    @property
    def image_data(self) -> str:
        return self.__settings['image_data']

    @property
    def bind_pnp_server(self) -> str:
        return self.__settings['bind_pnp_server']

    @property
    def port(self) -> int:
        return self.__settings['port']

    @property
    def time_format(self) -> str:
        return self.__settings['time_format']

    @property
    def status_refresh(self) -> int:
        return self.__settings['status_refresh']

    @property
    def debug(self) -> bool:
        return self.__settings['debug']

    @property
    def log_to_console(self) -> bool:
        return self.__settings['log_to_console']

    @property
    def log_file(self) -> str:
        return self.__settings['log_file']

    @property
    def image_url(self) -> str:
        return self.__settings['image_url']

    @property
    def config_url(self) -> str:
        return self.__settings['config_url']

    @property
    def default_cfg_file(self) -> str:
        return self.__settings['default_cfg_file']


class SoftwareImage:
    def __init__(self, image: str, version: str, md5: str, size: int,):
        self.image: str = image
        self.version: str = version
        self.md5: str = md5
        self.size: int = size


class ErrorCodes:
    __readable = {
        0: 'No error',
        100: 'unknown platform',
        101: 'no free space for update',
        102: 'unknown image',
        103: 'config file not found',
        104: 'image file not found',

        1412: 'Invalid input detected (config)',
        1413: 'Invalid input detected',
        1609: 'Error while retrieving device filesystem info',
        1816: 'Error verifying checksum for Image',
        1829: 'Image copy was unsuccessful',
        1803: 'Source file not found',
    }

    def __init__(self):
        self.ERROR_NO_ERROR = 0

        self.ERROR_NO_PLATFORM = 100
        self.ERROR_NO_FREE_SPACE = 101
        self.ERROR_NO_IMAGE = 102
        self.ERROR_NO_CFG_FILE = 103
        self.ERROR_NO_IMAGE_FILE = 104

        self.PNP_ERROR_INVALID_CONFIG = 1412
        self.PNP_ERROR_INVALID_INPUT = 1413
        self.PNP_ERROR_NO_FILESYSTEM_INFO = 1609
        self.PNP_ERROR_BAD_CHECKSUM = 1816
        self.PNP_ERROR_IMAGE_COPY_UNSUCCESSFUL = 1829
        self.PNP_ERROR_FILE_NOT_FOUND = 1803

    def readable(self, error_code: int):
        return self.__readable.get(error_code, f'unknown: {error_code}')


class PnpFlow:
    __readable = {
        0: 'None',
        1: 'new device',
        2: 'info',

        10: 'update required',
        11: 'update started',
        12: 'no update required/done',
        13: 'update done -> reloading',

        21: 'config start',
        22: 'config down -> reloading',
        23: 'reload for config update',

        99: 'finished',
    }

    def __init__(self):
        self.NONE = 0
        self.NEW = 1
        self.INFO = 2

        self.UPDATE_NEEDED = 10
        self.UPDATE_START = 11
        self.UPDATE_DOWN = 12
        self.UPDATE_RELOAD = 13

        self.CONFIG_START = 21
        self.CONFIG_DOWN = 22
        self.CONFIG_RELOAD = 23

        self.FINISHED = 99

    def readable(self, state: int):
        return self.__readable.get(state, 'unknown')


class Device:
    def __init__(self, udi: str, platform: str, hw_rev: str, serial: str, first_seen: str, last_contact: str,
                 src_address: str, current_job: str):

        self.udi: str = udi
        self.platform: str = platform
        self.hw_rev: str = hw_rev
        self.serial: str = serial
        self.ip_address: str = src_address
        self.current_job: str = current_job
        self.first_seen: str = first_seen
        self.last_contact: str = last_contact

        self.version: str = ''
        self.image: str = ''
        self.destination_name: str = ''
        self.destination_free: Optional[int] = None
        self.status: str = ''
        self.__pnp_flow: int = PNPFLOW.NEW
        self.pnp_flow_readable: str = PNPFLOW.readable(PNPFLOW.NEW)
        self.target_image: Optional[SoftwareImage] = None
        self.backoff: bool = False
        self.__refresh_data: bool = False
        self.refresh_button: str = ''
        self.__error_code: int = 0
        self.error_code_readable: str = ERROR.readable(ERROR.ERROR_NO_ERROR)
        self.error_count: int = 0
        self.error_message = ''
        self.__hard_error: bool = False
        self.__status_class: str = ''

    @property
    def pnp_flow(self) -> int:
        return self.__pnp_flow

    @pnp_flow.setter
    def pnp_flow(self, pnp_flow: int):
        self.__pnp_flow = pnp_flow
        self.pnp_flow_readable = PNPFLOW.readable(pnp_flow)
        if pnp_flow == PNPFLOW.FINISHED:
            self.__status_class = 'finished'

    @property
    def refresh_data(self) -> bool:
        return self.__refresh_data

    @refresh_data.setter
    def refresh_data(self, new_state: bool):
        self.__refresh_data = new_state
        if new_state:
            self.refresh_button = 'disabled='
        else:
            self.refresh_button = 'enabled='

    @property
    def error_code(self) -> int:
        return self.__error_code

    @error_code.setter
    def error_code(self, error_code: int):
        self.__error_code = error_code
        self.error_code_readable = ERROR.readable(error_code)
        self.__status_class = 'warning'

    @property
    def hard_error(self) -> bool:
        return self.__hard_error

    @hard_error.setter
    def hard_error(self, hard_error: bool):
        self.__hard_error = hard_error
        self.__status_class = 'error'

    @property
    def status_class(self) -> str:
        return self.__status_class

    @status_class.setter
    def status_class(self, status_class: str):
        self.__status_class = status_class


class Images:
    def __init__(self, images_file):
        self.__images = {}
        self.load_image_data(images_file)

    def load_image_data(self, images_file):
        try:
            with open(images_file, 'rb') as f:
                self.__images = toml_load(f)
        except FileNotFoundError as e:
            print(f'ERROR: Data file {images_file} not found! ({e})')
            exit(1)
        except TOMLDecodeError as e:
            print(f'ERROR: Data file {images_file} is not in valid toml format! ({e})')
            exit(2)

    @property
    def images(self) -> Dict[str, any]:
        return self.__images


def configure_logger(path):
    log_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(module)s ::%(message)s')
    log = logging.getLogger('root')
    log.setLevel(logging.INFO)

    log_file = path
    # create a new file > 5 mb size
    log_handler_file = RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=5 * 1024 * 1024,
        backupCount=10,
        # encoding=None,
        # delay=0
    )

    log_handler_file.setFormatter(log_formatter)
    log_handler_file.setLevel(logging.INFO)
    log.addHandler(log_handler_file)

    if SETTINGS.log_to_console:
        log_handler_console = logging.StreamHandler(stdout)
        log_handler_console.setFormatter(log_formatter)
        log_handler_console.setLevel(logging.INFO)
        log.addHandler(log_handler_console)


def log_info(message):
    if SETTINGS.debug:
        log = logging.getLogger('root')
        log.info(message)


def log_critical(message):
    if SETTINGS.debug:
        log = logging.getLogger('root')
        log.critical(message)


def parse_arguments() -> arg_Namespace:
    parser = ArgumentParser(
        prog='open-pnp.py',
        description='This is a basic implementation of the Cisco PnP protocol. It is intended to'
                    '\nroll out image updates and configurations for Cisco IOS/IOS-XE devices on day0.'
                    '\n'
                    f'\nVersion: {PNP_SERVER_VERSION}'
                    ', Written by: thl-cmk, for more information see: https://thl-cmk.hopto.org',
        formatter_class=RawTextHelpFormatter,
        epilog='Usage: python open-pnp.py --config_url  http://192.168.10.133:8080/configs '
               '--image_url http://192.168.10.133:8080/images',
    )
    parser.add_argument('-b', '--bind_pnp_server', type=str,
                        help='Bind PnP server to IP-address. (default: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int,
                        help='TCP port to listen on. (default: 8080)')
    parser.add_argument('-r', '--status_refresh', type=int,
                        help='Time in seconds to refresh PnP server status page. (default: 60)')
    parser.add_argument('--config_file', type=str,
                        help='Path/name of open PnP server config file. (default: open-pnp.toml)')
    parser.add_argument('--config_url', type=str,
                        help='Download URL for config files. I.e. http://192.168.10.133:8080/configs')
    parser.add_argument('--image_data', type=str,
                        help='File containing the image description. (default: images.toml)')
    parser.add_argument('--image_url', type=str,
                        help='Download URL for image files. I.e. http://192.168.10.133:8080/images')
    parser.add_argument('--debug', default=False, action="store_const", const=True,
                        help='Enable Debug output send to "log_file".')
    parser.add_argument('--log_file', type=str,
                        help='Path/name of the logfile. (default: log/pnp_debug.log, requires --debug) ')
    parser.add_argument('--log_to_console', default=False, action="store_const", const=True,
                        help='Enable debug output send to stdout (requires --debug).')
    parser.add_argument('--time_format', type=str,
                        help='Format string to render time. (default: %%Y-%%m-%%dT%%H:%%M:%%S)')

    return parser.parse_args()


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
    log_info(_template)
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
    log_info(_template)
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
    log_info(_template)
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
        log_info(_template)
        return _template
    else:
        device.error_code = ERROR.ERROR_NO_IMAGE_FILE
        device.hard_error = True


def pnp_config_upgrade(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    cfg_file = f'{device.serial}.cfg'
    response = head(f'{SETTINGS.config_url}/{cfg_file}')
    if response.status_code != 200:  # SERIAL.cfg not found
        cfg_file = SETTINGS.default_cfg_file
        response = head(f'{SETTINGS.config_url}/{cfg_file}')
        if response.status_code != 200:  # DEFAULT.cfg also not found
            device.error_code = ERROR.ERROR_NO_CFG_FILE
            device.hard_error = True
            return

    device.current_job = 'urn:cisco:pnp:device-info'
    device.pnp_flow = PNPFLOW.CONFIG_START
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
        'base_url': SETTINGS.config_url,
        'serial_number': cfg_file,
        'delay': 30,  # reload in seconds
        'cfg_file': cfg_file,
    }
    _template = render_template('config_upgrade.xml', **jinja_context)
    log_info(_template)
    return _template


def pnp_bye(udi: str, correlator: str) -> str:
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
    }
    _template = render_template('bye.xml', **jinja_context)
    log_info(_template)
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


def get_local_ip_addresses() -> List[str]:
    _addresses = []
    adapters = get_adapters()
    for adapter in adapters:
        ip_addr = ''
        for ip in adapter.ips:
            drop_ip = False
            if ip.is_IPv4:
                ip_addr = ip.ip
            elif ip.is_IPv6:
                ip_addr = ip.ip[0]
            for entry in ['127.', 'fe80::', '::1']:
                if str(ip_addr).lower().startswith(entry):
                    drop_ip = True
            if not drop_ip:
                _addresses.append(ip_addr)
    return _addresses


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
    log_info(f'REQUEST: {data}')
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
            log_info('BACKOFF')
            # backoff more and more on errors, max error_count = 11 -> 5 * 11 = 55
            # error_count == 12 -> like hard_error
            minutes = device.error_count + 1
            if minutes > 10:
                device.hard_error = True
            return Response(pnp_backoff(udi, correlator, minutes), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.NEW:
            log_info('PNPFLOW.NEW')
            device.pnp_flow = PNPFLOW.INFO
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_NEEDED:
            log_info('PNPFLOW.UPDATE_NEEDED')
            device.pnp_flow = PNPFLOW.UPDATE_START
            return Response(pnp_install_image(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_RELOAD:
            log_info('PNPFLOW.UPDATE_RELOAD')
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_DOWN:
            log_info('PNPFLOW.UPDATE_DOWN')
            return Response(pnp_config_upgrade(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.CONFIG_DOWN:  # will never reach this point, as pnp is removed bei EEM :-)
            log_info('PNPFLOW.CONFIG_DOWN')
            return Response(pnp_backoff_terminate(udi, correlator), mimetype='text/xml')
        log_info(f'Other PNP_FLOW: {PNPFLOW.readable(device.pnp_flow)}')
        return Response('', 200)
    else:
        log_info('REQUEST NEW DEVICE FOUND')
        create_new_device(udi, src_add)
        # return Response(device_info(udi, correlator, 'all'), mimetype='text/xml')
        devices[udi].pnp_flow = PNPFLOW.NEW
        return Response(pnp_backoff(udi, correlator), mimetype='text/xml')
        # return Response('', 200)


@app.route('/pnp/WORK-RESPONSE', methods=['POST'])
def pnp_work_response():
    data = xml_parse(request.data)
    log_info(f'RESPONSE: {data}')
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
        log_info(f'Correlator: {correlator}')
        log_info(f'Job type: {job_type}')
        log_info(f'PnP flow: {device.pnp_flow_readable}')
        log_info(f'Job status: {job_status}')
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
            log_info(_response)
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
    log_info('Empty Response')
    return Response('')


if __name__ == '__main__':

    ERROR = ErrorCodes()
    PNPFLOW = PnpFlow()
    SETTINGS = Settings(vars(parse_arguments()))
    SETTINGS.update(SETTINGS.cfg_file)
    IMAGES = Images(SETTINGS.image_data)

    devices: Dict[str, Device] = {}

    if SETTINGS.debug:
        app.debug = True
    else:
        # disable FLASK console output
        logging.getLogger("werkzeug").disabled = True
        cli.show_server_banner = lambda *args: None

    if SETTINGS.image_url == '':
        print(f'image_url not set, check {SETTINGS.cfg_file} or see open-pnp.py -h')
        exit(1)
    if SETTINGS.config_url == '':
        print(f'config_url not set, check {SETTINGS.cfg_file} or see open-pnp.py -h')
        exit(1)

    if SETTINGS.debug:
        configure_logger(SETTINGS.log_file)
        log_info('STARTED LOGGER')

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
    print(f'Writen by thl-cmk, see https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision')
    print()
    app.run(host=SETTINGS.bind_pnp_server, port=SETTINGS.port)
