#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2023-02-26
# File  : open_pnp_utils.py

#
# 2023-03-13: added --no-default-cfg option
#

from typing import List
import logging
from logging.handlers import RotatingFileHandler
from sys import stdout
from argparse import (
    Namespace as arg_Namespace,
    ArgumentParser,
    RawTextHelpFormatter,
)
from ifaddr import get_adapters


def configure_logger(path: str, log_to_console: bool):
    log_formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(name)s :: %(module)s ::%(message)s')
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

    if log_to_console:
        log_handler_console = logging.StreamHandler(stdout)
        log_handler_console.setFormatter(log_formatter)
        log_handler_console.setLevel(logging.INFO)
        log.addHandler(log_handler_console)


def log_info(message: str, debug: bool):
    if debug:
        log = logging.getLogger('root')
        log.info(message)


def log_critical(message: str, debug: bool):
    if debug:
        log = logging.getLogger('root')
        log.critical(message)


def parse_arguments(pnp_server_version: str) -> arg_Namespace:
    parser = ArgumentParser(
        prog='open-pnp.py',
        description='This is a basic implementation of the Cisco PnP protocol. It is intended to'
                    '\nroll out image updates and configurations for Cisco IOS/IOS-XE devices on day0.'
                    '\n'
                    f'\n{pnp_server_version} | Written by: thl-cmk, for more information see: https://thl-cmk.hopto.org',
        formatter_class=RawTextHelpFormatter,
        epilog='Usage: python open-pnp.py --config-url  http://192.168.10.133:8080/configs '
               '--image-url http://192.168.10.133:8080/images',
    )
    parser.add_argument('-b', '--bind-pnp-server', type=str,
                        help='Bind PnP server to IP-address. (default: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int,
                        help='TCP port to listen on. (default: 8080)')
    parser.add_argument('-r', '--status-refresh', type=int,
                        help='Time in seconds to refresh PnP server status page. (default: 60)')
    parser.add_argument('-v', '--version', default=False, action='store_const', const=True,
                        help='Print open-pnp-server version and exit')
    parser.add_argument('--config-file', type=str,
                        help='Path/name of open PnP server config file. (default: open-pnp.toml)')
    parser.add_argument('--config-url', type=str,
                        help='Download URL for config files. I.e. http://192.168.10.133:8080/configs')
    parser.add_argument('--image-data', type=str,
                        help='File containing the image description. (default: images.toml)')
    parser.add_argument('--mapping-file', '--inventory-file', dest='mapping_file', type=str,
                        help='CSV mapping file used to map serial numbers to hostnames.')
    parser.add_argument('--state-file', type=str,
                        help='JSON state file used to persist devices between server restarts.')
    parser.add_argument('--image-url', type=str,
                        help='Download URL for image files. I.e. http://192.168.10.133:8080/images')
    parser.add_argument('--debug', default=False, action='store_const', const=True,
                        help='Enable Debug output send to "log-file".')
    parser.add_argument('--default-cfg', type=str,
                        help='default config to use if no device specific config is found. (default: DEFAULT.cfg)')
    parser.add_argument('--no-default-cfg', default=False, action='store_const', const=True,
                        help='Disables default config file for PnP devices. This option takes precedence over all '
                             '"--default-cfg" cli options or config entries.')
    parser.add_argument('--log-file', type=str,
                        help='Path/name of the logfile. (default: log/pnp_debug.log, requires --debug) ')
    parser.add_argument('--log-to-console', default=False, action='store_const', const=True,
                        help='Enable debug output send to stdout (requires --debug).')
    parser.add_argument('--time-format', type=str,
                        help='Format string to render time. (default: %%Y-%%m-%%dT%%H:%%M:%%S)')

    return parser.parse_args()


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
