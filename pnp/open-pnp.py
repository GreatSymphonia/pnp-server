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
# 20-12-14: added count in status page
#           added check if image/config file available
# 20-12-15: renamed ./vars/vars.py to ./vars/settings.py
#           stop on import error for images.py and platforms.py
#           removed extending path variable to ./vars

import re
from flask import Flask, request, send_from_directory, render_template, Response, redirect, cli
from pathlib import Path
import xmltodict
from time import strftime
from typing import Optional, List, Dict, Any
import logging
from logging.handlers import RotatingFileHandler
from requests import head

try:
    from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
    _netifaces = True
except ModuleNotFoundError:
    _netifaces = False
    pass


BIND_PNP_SERVER = '0.0.0.0'
PORT = 8080
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
STATUS_REFRESH = 60
DEBUG = False
LOG_TO_FILE = True
LOG_FILE = 'log/pnp_debug.log'
IMAGE_BASE_URL = ''
CONFIG_BASE_URL = ''

IMAGES = {}
PLATFORMS = {}

# import global variables
try:
    from vars.settings import *
except ModuleNotFoundError:
    pass

try:
    from vars.images import *
    from vars.platforms import *
except ModuleNotFoundError as e:
    print(f'{e}')
    exit(1)

CONFIG_BASE_URL = CONFIG_BASE_URL.rstrip('/')
IMAGE_BASE_URL = IMAGE_BASE_URL.rstrip('/')


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


ERROR = ErrorCodes()


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


PNPFLOW = PnpFlow()


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


app = Flask(__name__, template_folder='./templates')
if DEBUG:
    app.debug = True
else:
    # disable FLASK console output
    logging.getLogger("werkzeug").disabled = True
    cli.show_server_banner = lambda *args: None


current_dir = Path(__file__)
devices: Dict[str, Device] = {}


def configure_logger(path):
    log_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(module)s ::%(message)s')
    log_file = path
    # create a new file > 5 mb size
    log_handler = RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=5 * 1024 * 1024,
        backupCount=10,
        # encoding=None,
        # delay=0
    )
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    log = logging.getLogger('root')
    log.setLevel(logging.INFO)
    log.addHandler(log_handler)


def log_info(message):
    if LOG_TO_FILE:
        log = logging.getLogger('root')
        log.info(message)


def log_critical(message):
    if LOG_TO_FILE:
        log = logging.getLogger('root')
        log.critical(message)


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
    if DEBUG:
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
    if DEBUG:
        log_info(_template)
    return _template


# will not be used as we remove PNP via EEM. PNP terminate is missing a "write mem"
def pnp_backoff_terminate(udi: str, correlator: str) -> str:
    device = devices[udi]
    device.status = f'finished'
    device.pnp_floe = PNPFLOW.FINISHED
    device.current_job = 'urn:cisco:pnp:backoff-terminate'
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
    }
    _template = render_template('backoff_terminate.xml', **jinja_context)
    if DEBUG:
        log_info(_template)
    return _template


def pnp_install_image(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    response = head(f'{IMAGE_BASE_URL}/{device.target_image.image}')
    if response.status_code == 200:
        device.current_job = 'urn:cisco:pnp:image-install'
        device.pnp_flow = PNPFLOW.UPDATE_START
        device.backoff = True
        device.refresh_data = True
        jinja_context = {
            'udi': udi,
            'correlator': correlator,
            'base_url': IMAGE_BASE_URL,
            'image': device.target_image.image,
            'md5': device.target_image.md5.lower(),
            'destination': device.destination_name,
            'delay': 0,  # reload in seconds
        }
        _template = render_template('image_install.xml', **jinja_context)
        if DEBUG:
            log_info(_template)
        return _template
    else:
        device.error_code = ERROR.ERROR_NO_IMAGE_FILE
        device.hard_error = True


def pnp_config_upgrade(udi: str, correlator: str) -> Optional[str]:
    device = devices[udi]
    response = head(f'{CONFIG_BASE_URL}/{device.serial}.cfg')
    if response.status_code == 200:
        device.current_job = 'urn:cisco:pnp:device-info'
        device.pnp_flow = PNPFLOW.CONFIG_START
        jinja_context = {
            'udi': udi,
            'correlator': correlator,
            'base_url': CONFIG_BASE_URL,
            'serial_number': device.serial,
            'delay': 0,  # reload in seconds
        }
        _template = render_template('config_upgrade.xml', **jinja_context)
        if DEBUG:
            log_info(_template)
        return _template
    else:
        device.error_code = ERROR.ERROR_NO_CFG_FILE
        device.hard_error = True


def pnp_bye(udi: str, correlator: str) -> str:
    jinja_context = {
        'udi': udi,
        'correlator': correlator,
    }
    _template = render_template('bye.xml', **jinja_context)
    if DEBUG:
        log_info(_template)
    return _template


SERIAL_NUM_RE = re.compile(r'PID:(?P<product_id>\w+(?:-\w+)*),VID:(?P<hw_version>\w+),SN:(?P<serial_number>\w+)')


def create_new_device(udi: str, src_add: str):
    platform, hw_rev, serial = SERIAL_NUM_RE.findall(udi)[0]
    devices[udi] = Device(
        udi=udi,
        first_seen=strftime(TIME_FORMAT),
        last_contact=strftime(TIME_FORMAT),
        src_address=src_add,
        serial=serial,
        platform=platform,
        hw_rev=hw_rev,
        current_job='urn:cisco:pnp:device-info',
    )
    device = devices[udi]
    device.backoff = True
    if device.platform in PLATFORMS:
        platform = PLATFORMS[device.platform]
        if platform.image in IMAGES:
            device.target_image = IMAGES[platform.image]
        else:
            device.error_code = ERROR.ERROR_NO_IMAGE
            device.hard_error = True
    else:
        device.error_code = ERROR.ERROR_NO_PLATFORM
        device.hard_error = True


def update_device_info(data: Dict[str, Any]):
    destination = {}

    udi = data['pnp']['@udi']
    device = devices[udi]

    device.version = data['pnp']['response']['imageInfo']['versionString']
    device.image = data['pnp']['response']['imageInfo']['imageFile'].split(':')[1]
    device.refresh_data = False
    device.last_contact = strftime(TIME_FORMAT)
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
    for iface_name in interfaces():
        try:
            for _address in ifaddresses(iface_name).setdefault(AF_INET):
                _addresses.append(_address['addr'])
        except TypeError:
            pass
        try:
            for _address in ifaddresses(iface_name).setdefault(AF_INET6):
                _addresses.append(_address['addr'])
        except TypeError:  # if no ip address in interface ifaddresses(iface_name) comes back with None
            pass
    return _addresses


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
        'refresh': STATUS_REFRESH,
        'config_base_url': CONFIG_BASE_URL,
        'image_base_url': IMAGE_BASE_URL,
    }
    if DEBUG:
        result = render_template('status_debug.html', **jinja_context)
    else:
        result = render_template('status.html', **jinja_context)
    return Response(result)


@app.route('/buttons', methods=['POST'])
def buttons():
    udi = list(request.form.keys())[0]
    button = list(request.form.values())[0]

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
    data = xmltodict.parse(request.data)
    if DEBUG:
        log_info(f'REQUEST: {data}')
    correlator = data['pnp']['info']['@correlator']
    udi = data['pnp']['@udi']
    if udi in devices.keys():
        device = devices[udi]
        device.last_contact = strftime(TIME_FORMAT)
        device.ip_address = src_add
        if device.hard_error:
            return Response(pnp_backoff(udi, correlator, 59), mimetype='text/xml')
            pass
        if device.backoff:
            if DEBUG:
                log_info('BACKOFF')
            # backoff more and more on errors, max error_count = 11 -> 5 * 11 = 55
            # error_count == 12 -> like hard_error
            minutes = min((device.error_count * 5), 57) + 2
            if minutes > 57:
                device.hard_error = True
            return Response(pnp_backoff(udi, correlator, minutes), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.NEW:
            if DEBUG:
                log_info('PNPFLOW.NEW')
            device.pnp_flow = PNPFLOW.INFO
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_NEEDED:
            if DEBUG:
                log_info('PNPFLOW.UPDATE_NEEDED')
            device.pnp_flow = PNPFLOW.UPDATE_START
            return Response(pnp_install_image(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_RELOAD:
            if DEBUG:
                log_info('PNPFLOW.UPDATE_RELOAD')
            return Response(pnp_device_info(udi, correlator, 'all'), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.UPDATE_DOWN:
            if DEBUG:
                log_info('PNPFLOW.UPDATE_DOWN')
            return Response(pnp_config_upgrade(udi, correlator), mimetype='text/xml')
        if device.pnp_flow == PNPFLOW.CONFIG_DOWN:  # will never reach this point, as pnp is removed bei EEM :-)
            if DEBUG:
                log_info('PNPFLOW.CONFIG_DOWN')
            return Response(pnp_backoff_terminate(udi, correlator), mimetype='text/xml')
        if DEBUG:
            log_info(f'Other PNP_FLOW: {device.pnp_flow}')
        return Response('', 200)
    else:
        if DEBUG:
            log_info('REQUEST NEW DEVICE FOUND')
        create_new_device(udi, src_add)
        # return Response(device_info(udi, correlator, 'all'), mimetype='text/xml')
        devices[udi].pnp_flow = PNPFLOW.NEW
        return Response(pnp_backoff(udi, correlator), mimetype='text/xml')
        # return Response('', 200)


@app.route('/pnp/WORK-RESPONSE', methods=['POST'])
def pnp_work_response():
    data = xmltodict.parse(request.data)
    if DEBUG:
        log_info(f'RESPONSE: {data}')
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    udi = data['pnp']['@udi']
    job_type = data['pnp']['response']['@xmlns']
    if udi not in devices.keys():
        create_new_device(udi, src_add)

    device = devices[udi]
    device.ip_address = src_add
    device.last_contact = strftime(TIME_FORMAT)

    if job_type == 'urn:cisco:pnp:fault':  # error without job info (correlator):-(
        device.error = data['pnp']['response']['fault']['detail']['XSVC-ERR:error']['XSVC-ERR:details']
    else:
        correlator = data['pnp']['response']['@correlator']
        job_status = int(data['pnp']['response']['@success'])
        if DEBUG:
            log_info(correlator)
            log_info(job_type)
            log_info(device.pnp_flow_readable)
            log_info(job_status)
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
            if DEBUG:
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
    if DEBUG:
        log_info('Empty Response')
    return Response('')


if __name__ == '__main__':
    if IMAGE_BASE_URL == '':
        print('IMAGE_BASE_URL not set, check ./vars/vars.py')
        exit(1)
    if CONFIG_BASE_URL == '':
        print('CONFIG_BASE_URL not set, check ./vars/vars.py')
        exit(1)

    if DEBUG:
        configure_logger(LOG_FILE)
        log_info('STARTED LOGGER')

    print()
    print('Running PnP server. Stop with ctrl+c')
    print(f'Bind to IP-address      : {BIND_PNP_SERVER}')
    print(f'Listen on port          : {PORT}')
    print(f'Image file(s) base URL  : {IMAGE_BASE_URL}')
    print(f'Config file(s) base URL : {CONFIG_BASE_URL}')
    print()
    if _netifaces:
        print('The PnP server is running on the following URL(s)')
        if BIND_PNP_SERVER in ['0.0.0.0', '::']:
            addresses = get_local_ip_addresses()
            for address in addresses:
                print(f'    http://{address}:{PORT}')
        else:
            print(f'Status page running on : http://{BIND_PNP_SERVER}:{PORT}')
        print()
    app.run(host=BIND_PNP_SERVER, port=PORT)
