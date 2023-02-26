#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2023-02-26
# File  : open_pnp_classes.py


from typing import Dict, Optional, Any
from tomli import load as toml_load
from tomli import TOMLDecodeError


class Settings:
    def __init__(
            self,
            cli_args: Dict[str, Any],
            version: bool = False,
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
            default_cfg: Optional[str] = 'DEFAULT.cfg',
    ):
        self.__settings = {
            'cfg_file': cfg_file,
            'version': version,
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
            'default_cfg_file': default_cfg,
        }
        self.__args = {}
        self.__set_cli_args(cli_args)

    def __set_cli_args(self, cli_args: Dict[str, Any]):
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
            print(
                f'ERROR: Data file {cfg_file} is not in valid toml format! ({e})')
            exit(2)

        self.__settings.update(self.__args)

    @property
    def cfg_file(self) -> str:
        return self.__settings['cfg_file']

    @property
    def version(self) -> bool:
        return self.__settings['version']

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
    def default_cfg(self) -> str:
        return self.__settings['default_cfg']


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

        30: 'cleanup required',
        31: 'cleanup started',
        32: 'no cleanup required/done',

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

        self.CLEANUP_NEEDED = 30
        self.CLEANUP_START = 31
        self.CLEANUP_DOWN = 32

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
            print(
                f'ERROR: Data file {images_file} is not in valid toml format! ({e})')
            exit(2)

    @property
    def images(self) -> Dict[str, Any]:
        return self.__images

ERROR = ErrorCodes()
PNPFLOW = PnpFlow()
