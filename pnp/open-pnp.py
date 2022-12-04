#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2022-12-03
# File  : open-pnp.py
#
# Basic Cisco PnP server for Day0 provisioning
#
# based on https://github.com/oliverl-21/Open-PnP-Server
#
# Cisco doc on https://developer.cisco.com/site/open-plug-n-play/learn/learn-open-pnp-protocol/
#

import re
from flask import Flask, request, send_from_directory, render_template, Response, redirect
from pathlib import Path
import sys
import xmltodict
import time
from typing import Optional

BIND_PNP_SERVER = '0.0.0.0'
PORT = 8080
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%Z'
STATUS_REFRESH = 10
IMAGE_BASE_URL = ''
CONFIG_BASE_URL = ''
IMAGES = {}
PLATFORMS = {}

# import global variables
sys.path.append('./vars')
try:
    from vars import *
    from images import *
    from platforms import *
except ModuleNotFoundError:
    pass


class State:
    __state_desc = {
        0: 'new device',
        1: 'info',

        10: 'update needed',
        11: 'update stated',
        12: 'update done/not needed',
        13: 'reload for image update',

        100: 'unknown platform',
        101: 'no free space for update',
        102: 'unknown image',
    }

    def __init__(self):
        self.NEW = 0
        self.INFO = 1

        self.UPDATE_NEEDED = 10
        self.UPDATE_START = 11
        self.UPDATE_DOWN = 12
        self.UPDATE_RELOAD = 13

        self.ERROR_NO_PLATFORM = 100
        self.ERROR_NO_FREE_SPACE = 101
        self.ERROR_NO_IMAGE = 102

    def state_readable(self, state: int):
        return self.__state_desc.get(state, 'unknown')


class Device:
    def __init__(self, udi: str, platform: str, hw_rev: str, serial: str, first_seen: str, last_contact: str,
                 src_address: str, current_job: str):

        self.udi: str = udi
        self.platform: str = platform
        self.hw_rev: str = hw_rev
        self.serial: str = serial
        self.src_address: str = src_address
        self.current_job: str = current_job
        self.first_seen: str = first_seen
        self.last_contact: str = last_contact

        self.version: str = ''
        self.image: str = ''
        self.destination_name: str = ''
        self.destination_free: int = 0
        self.__state: int = 0
        self.state_readable: str = State().state_readable(0)
        self.error: str = ''
        self.target_image: Optional[SoftwareImage] = None
        self.backoff_count: int = 0
        self.__refresh_data: bool = False
        self.refresh_button: str = ''

    @property
    def state(self) -> int:
        return self.__state

    @state.setter
    def state(self, new_state: int):
        self.__state = new_state
        self.state_readable = State().state_readable(self.__state)

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


app = Flask(__name__, template_folder='./templates')
app.debug = True

current_dir = Path(__file__)
devices: [str, Device] = {}


def get_device_info(udi: str, correlator_id: str, info_type: str) -> str:
    # info_type can be one of:
    # image, hardware, filesystem, udi, profile, all
    if devices[udi].current_job != 'urn:cisco:pnp:image-install':
        devices[udi].current_job = 'urn:cisco:pnp:device-info'
    jinja_context = {
        'udi': udi,
        'correlator_id': correlator_id,
        'info_type': info_type
    }
    return render_template('device_info.xml', **jinja_context)


def back_off(udi: str, correlator_id: str) -> str:
    # seconds min: 0, max: 59
    backoff_seconds = 59
    devices[udi].status = f'back off {backoff_seconds}s'
    devices[udi].current_job = 'urn:cisco:pnp:backoff'
    jinja_context = {
        'udi': udi,
        'correlator_id': correlator_id,
        'seconds': backoff_seconds
    }
    return render_template('backoff.xml', **jinja_context)


def install_image(udi: str, correlator_id: str) -> str:
    device = devices[udi]
    device.current_job = 'urn:cisco:pnp:image-install'
    device.state = State().UPDATE_START
    device.refresh_data = True
    jinja_context = {
        'udi': udi,
        'correlator_id': correlator_id,
        'http_server': IMAGE_BASE_URL,
        'image': device.target_image.image,
        'md5': device.target_image.md5,
        'destination': device.destination_name,
        'delay': 0,  # seconds
    }
    return render_template('image.xml', **jinja_context)


def load_config(udi: str, correlator_id: str, serial_number: str) -> str:
    jinja_context = {
        'udi': udi,
        'correlator_id': correlator_id,
        'http_server': CONFIG_BASE_URL,
        'serial_number': serial_number,
    }
    return render_template('load_config.xml', **jinja_context)


def bye(udi: str, correlator_id: str) -> str:
    jinja_context = {
        'udi': udi,
        'correlator_id': correlator_id,
    }
    return render_template('bye.xml', **jinja_context)


SERIAL_NUM_RE = re.compile(r'PID:(?P<product_id>\w+(?:-\w+)*),VID:(?P<hw_version>\w+),SN:(?P<serial_number>\w+)')


def create_new_device(udi: str, src_add: str):
    platform, hw_rev, serial = SERIAL_NUM_RE.findall(udi)[0]
    devices[udi] = Device(
        udi=udi,
        first_seen=time.strftime(TIME_FORMAT),
        last_contact=time.strftime(TIME_FORMAT),
        src_address=src_add,
        serial=serial,
        platform=platform,
        hw_rev=hw_rev,
        current_job='urn:cisco:pnp:device-info',
    )
    device = devices[udi]
    if device.platform in PLATFORMS:
        platform = PLATFORMS[device.platform]
        if platform.image in IMAGES:
            device.target_image = IMAGES[platform.image]
        else:
            device.last_error = 'unknown target image'
            device.state = State().ERROR_NO_IMAGE
    else:
        device.last_error = 'unknown device type'
        device.state = State().ERROR_NO_PLATFORM


def update_device_info(data: [str, str]):
    destination = {}

    udi = data['pnp']['@udi']
    device = devices[udi]

    device.version = data['pnp']['response']['imageInfo']['versionString']
    device.image = data['pnp']['response']['imageInfo']['imageFile'].split(':')[1]
    device.refresh_data = False
    device.last_contact = time.strftime(TIME_FORMAT)

    if device.state == State().UPDATE_START:

        if device.version == device.target_image.version:
            device.state = State().UPDATE_DOWN
    else:
        for filesystem in data['pnp']['response']['fileSystemList']['fileSystem']:
            if filesystem['@name'] in ['bootflash', 'flash']:
                destination = filesystem

        device.platform = data['pnp']['response']['hardwareInfo']['platformName']
        device.serial = data['pnp']['response']['hardwareInfo']['boardId']
        device.destination_name = destination['@name']
        device.destination_free = int(destination['@freespace'])


def check_update(udi:str):
    device = devices[udi]
    if device.image == device.target_image.image:
        device.state = State().UPDATE_DOWN
    else:
        device.state = State().UPDATE_NEEDED
        if device.destination_free < device.target_image.size:
            _mb = round(device.target_image.size / 1024 / 1024)
            device.last_error = f'no space on device, need {_mb} MBytes'
            device.state = State().ERROR_NO_FREE_SPACE


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
    }
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
            device.last_error = None

    return redirect('/status', 302)


@app.route('/configs/<path:path>')
def serve_configs(path):
    print(path)
    return send_from_directory('configs', path)


@app.route('/images/<path:path>')
def serve_sw_images(path):
    return send_from_directory('images', path)


@app.route('/pnp/HELLO')
def pnp_hello():
    return '', 200


@app.route('/pnp/WORK-REQUEST', methods=['POST'])
def pnp_work_request():
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    data = xmltodict.parse(request.data)
    correlator_id = data['pnp']['info']['@correlator']
    udi = data['pnp']['@udi']
    if udi in devices.keys():
        device = devices[udi]
        device.last_contact = time.strftime(TIME_FORMAT)
        device.src_address = src_add
        if device.state == State().NEW or device.refresh_data:
            return Response(get_device_info(udi, correlator_id, 'all'), mimetype='text/xml')
        if device.state == State().UPDATE_NEEDED:
            return Response(install_image(udi, correlator_id), mimetype='text/xml')
        if device.backoff_count > 0:
            device.backoff_count -= 1
            return Response(back_off(udi, correlator_id), mimetype='text/xml')
        if device.state == State().UPDATE_RELOAD:
            return Response(get_device_info(udi, correlator_id, 'all'), mimetype='text/xml')
        return Response('', 200)
    else:
        create_new_device(udi, src_add)
        return Response(get_device_info(udi, correlator_id, 'all'), mimetype='text/xml')


@app.route('/pnp/WORK-RESPONSE', methods=['POST'])
def pnp_work_response():
    data = xmltodict.parse(request.data)
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    udi = data['pnp']['@udi']
    job_type = data['pnp']['response']['@xmlns']
    correlator_id = data['pnp']['response']['@correlator']

    if udi not in devices.keys():
        create_new_device(udi, src_add)

    device = devices[udi]
    device.src_address = src_add
    device.last_contact = time.strftime(TIME_FORMAT)

    if job_type == 'urn:cisco:pnp:fault':
        print(data)
        device.error = data['pnp']['response']['fault']['detail']['XSVC-ERR:error']['XSVC-ERR:details']
    else:
        job_status = int(data['pnp']['response']['@success'])
        if job_status == 1:
            if job_type == 'urn:cisco:pnp:device-info':
                update_device_info(data)
                device.current_job = 'none'
                if device.state not in [State().UPDATE_START]:
                    check_update(udi)
            elif job_type == 'urn:cisco:pnp:image-install':
                device.state = State().UPDATE_RELOAD
                device.backoff_count = 10
                device.current_job = 'none'
            elif job_type == 'urn:cisco:pnp:backoff':
                device.current_job = 'none'
        elif job_status == 0:
            device.last_error = data['pnp']['response']['errorInfo']['errorMessage']
            print(data)
    return Response(bye(udi, correlator_id), mimetype='text/xml')


if __name__ == '__main__':
    if IMAGE_BASE_URL == '':
        print('IMAGE_BASE_URL not set, check ./vars/vars.py')
        exit(1)
    if CONFIG_BASE_URL == '':
        print('CONFIG_BASE_URL not set, check ./vars/vars.py')
        exit(1)

    app.run(host=BIND_PNP_SERVER, port=PORT)
