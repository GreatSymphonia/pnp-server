#!/usr/bin/env python
# -*- coding: utf-8 -*-

# based on https://github.com/cisco-ie/IOSXE_ZTP

#
# keep python2 compatible for older IOS-XE versions (incl. 17.1 :-( )
# - don't use f-strings
# - no type hinting
#
# known issues
#
#  Version      Model       Issue
#  17.01.01a    ISR1100     Works only on Gi0/0/0 (WAN IF), no DHCP requests on switch ports seen
#  17.09.01a    ISR1100     Guest shell is not included in the image, is now a separate package,
#                           need way for  install/autostart
#  17.04.02     ISR1100     "install add file <image> activate commit prompt-level none" issues a write mem
#                           -> no last run to push the config, Workaround: install_mode = False

#  all          all         don't set the dhcp lease time lower than the the time needed for the image transfer
#
# WLC C9800 show version
# https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/217050-convert-installation-mode-between-instal.html
# Installation mode is BUNDLE
# Installation mode is INSTALL


# Importing cli module
from cli import cli, configure, configurep, execute, executep
import re
import time
import sys
import logging
from logging.handlers import RotatingFileHandler


class SoftwareImage:
    def __init__(self, image, version, md5_image, guestshell=None, md5_guestshell=None, install_mode=True):
        self.image = image
        self.version = version
        self.md5_image = md5_image
        self.guestshell = guestshell
        self.md5_guestshell = md5_guestshell
        self.install_mode = install_mode


class Model:
    def __init__(self, family, model, install_mode=True):
        self.family = family
        self.model = model
        self.install_mode = install_mode


software_images = {
    'CAT9K': SoftwareImage(
        image='cat9k_iosxe.17.06.01.SPA.bin',
        version='17.06.01',
        md5_image='fdb9c92bae37f9130d0ee6761afe2919',
    ),
    'ASR1000': SoftwareImage(
        image='asr1000-universalk9.17.05.01a.SPA.bin',
        version='17.05.01a',
        md5_image='0e4b1fc1448f8ee289634a41f75dc215',
    ),
    'C1100_16_12': SoftwareImage(
        image='c1100-universalk9.16.12.01a.SPA.bin',
        version='16.12.01a',
        md5_image='045d73625025b4f77c65c7800b7faa2b',
    ),
    'C1100_17_01': SoftwareImage(
        image='c1100-universalk9.17.01.01.SPA.bin',
        version='17.01.01',
        md5_image='62e79c54994b82fc862c2ca043dcd543',
        install_mode=False,  # guestshell don't work in install mode
    ),
    'C1100_17_02': SoftwareImage(
        image='c1100-universalk9.17.02.03.SPA.bin',
        version='17.02.03',
        md5_image='4986d253b333d21b1b80c76f6d2267ca',
    ),
    'C1100_17_03': SoftwareImage(
        image='c1100-universalk9.17.03.05.SPA.bin',
        version='17.03.05',
        md5_image='64aa0df0806f7f962d66d325ff917e4a',
    ),
    'C1100_17_04': SoftwareImage(
        image='c1100-universalk9.17.04.02.SPA.bin',
        version='17.04.02',
        md5_image='40b7ec81c4e4cdc8b3683a3938ae8361',
        install_mode=False  # issues wr mem on install add so no round 3
    ),
    'C1100_17_05': SoftwareImage(
        image='c1100-universalk9.17.05.01a.SPA.bin',
        version='17.05.01a',
        md5_image='85d86916e33d27ae9867eec822206b97',
    ),
    'C1100_17_06_03': SoftwareImage(
        image='c1100-universalk9.17.06.03a.SPA.bin',
        version='17.06.03a',
        md5_image='2501b21b6fa3f71ea6acd7d59bcc8423',
        install_mode=False,
    ),
    'C1100_17_06_04': SoftwareImage(
        image='c1100-universalk9.17.06.04.SPA.bin',
        version='17.06.04',
        md5_image='2caa962f5ed0ecc52f99b90c733c54de',
    ),
    'C1100_17_07': SoftwareImage(
        image='c1100-universalk9.17.07.02.SPA.bin',
        version='17.07.02',
        md5_image='b824743e09cfa2644ccb442ef3e48cd2',
    ),
    'C1100_17_08': SoftwareImage(
        image='c1100-universalk9.17.08.01a.SPA.bin',
        version='17.08.01a',
        md5_image='8997c56cb03b5dcb08f12bf82fe23988',
    ),
    'C1100_17_09': SoftwareImage(
        image='c1100-universalk9.17.09.01a.SPA.bin 17.09.01a',
        version='17.09.01a',
        md5_image='b3efb230d869fa6e77a98b4130c89585',
        guestshell='guestshell.17.09.01a.tar',
        md5_guestshell='13276a9ff54bef3748416f404d92da09',
    ),
}

models = {
    'C9300-24P': Model(
        family='CAT9K',
        model='C9300-24P',
    ),
    'C9500-24Q': Model(
        family='CAT9K',
        model='C9500-24Q',
    ),
    'ASR1001-HX': Model(
        family='ASR1000',
        model='ASR1001-HX',
    ),
    'C1117-4PMLTEEAWE': Model(
        family='C1100_17_06_04',
        model='C1117-4PMLTEEAWE',
        # install_mode=False,
    ),
}

# global variables
http_image = '192.168.10.15'
http_config = '192.168.10.15'
ntp_server = '10.10.10.1'
syslog_server = '10.10.10.1'
# log level:
#   0 - emergencies
#   1 - alerts
#   2 - critical
#   3 - errors
#   4 - warning
#   5 - notifications
#   6 - informational
#   7 - debugging
console_log_level = 'emergencies'
log_to_file = True
no_md5_verify = ['16.06', '16.07']  # do not verify image if version in this list? Why?
reload_in = 2
switch_to_install_mode = True
verbose = False

if verbose:
    _configure = configurep
    _execute = executep
else:
    _configure = configure
    _execute = executep


class Device:
    def __init__(self):
        self.model = None
        self.serial = None
        self.current_version = None
        self.install_mode = None
        self.needs_startup = False
        self.flash_size = 0
        self.__show_version = cli('show version')
        self.__show_startup = cli('show startup-config')
        self.__show_file_system = cli('show file system')

        # get model
        try:
            self.model = re.search(r'Model Number\s+:\s+(\S+)', self.__show_version).group(1)
        except AttributeError:
            self.model = re.search(r'cisco\s(\w+-.*?)\s', self.__show_version).group(1)

        # get serial number
        try:
            self.serial = re.search(r'System Serial Number\s+:\s+(\S+)', self.__show_version).group(1)
        except AttributeError:
            self.serial = re.search(r'Processor board ID\s+(\S+)', self.__show_version).group(1)

        # get current version
        self.current_version = re.search(r'Cisco IOS XE Software, Version\s+(\S+)', self.__show_version).group(1)

        # get install mode on WLC C9800
        try:
            self.install_mode = re.search(r'Installation mode is\s+(\S+)',
                                          self.__show_version).group(1).endswith('INSTALL')
        except AttributeError:
            # get install mode (in bundle mode System image file equals image file name)
            self.install_mode = re.search(r'System image file is\s+(\S+)',
                                          self.__show_version).group(1).endswith(':packages.conf"')

        self.needs_startup = True if 'startup-config is not present' in self.__show_startup else False

        # init flash size
        self.get_flash_free()

    def get_usb_present(self):
        self.__show_file_system = cli('show file systems')
        return True if 'usb0:' in self.__show_file_system else False

    def get_flash_free(self):
        self.__show_file_system = cli('show file systems')
        try:
            self.flash_size, _flash_free = re.search(r'(\d+)\s+(\d+).+bootflash:.*', self.__show_file_system).groups()
            self.flash_size = int(self.flash_size)
        except AttributeError:
            self.flash_size = 0
            return 0
        return int(_flash_free)


def main():
    pre_conf = [
        'logging console ' + console_log_level,
        'logging buffered 100000',
        'file prompt quiet',
        'no ip domain lookup',
        'line con 0',
        'logging synchronous',
        'width 150',
    ]
    if ntp_server:
        pre_conf += [
            # don't set time zone to be in sync with guestshell
            # 'clock timezone CET 1 0',
            # 'clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00',
            'ntp server ' + ntp_server,
        ]
    if syslog_server:
        pre_conf += [
            'logging host ' + syslog_server,
            'logging trap debug',
            'logging count',
            'logging on',
        ]
    _configure(pre_conf)

    try:
        # switch to enable/disable persistent logger
        if log_to_file:
            filepath = create_logfile()
            print('Log file created in : ' + filepath)
            configure_logger(filepath)

        log_info('###### STARTING ZTP SCRIPT ######')
        print('')
        log_info('Python version................: ' + sys.version.replace('\n', ' '))
        print('')

        log_info('Getting device info')
        device = Device()

        log_info('Model..........................: ' + device.model)
        log_info('Serial number..................: ' + device.serial)
        log_info('Current version................: ' + device.current_version)
        log_info('Install mode...................: ' + str(device.install_mode))
        log_info('Flash size/free (MB)...........: ' + str(round(device.flash_size / 1024 / 1024)) + '/' +
                 str(round(device.get_flash_free() / 1024 / 1024)))
        log_info('USB present....................: ' + str(device.get_usb_present()))

        if device.model not in models.keys():
            log_info('Model: ' + device.model + ' not found in ZTP script data. Stopping ZTP....')
            sys.exit()

        model = models[device.model]

        if model.family not in software_images.keys():
            log_info('Image family: ' + model.family + ' not found in ZTP script data. Stopping ZTP....')
            sys.exit()

        target_software = software_images[model.family]
        print('')
        log_info('Target image data')
        log_info('Image..........................: ' + target_software.image)
        log_info('Version........................: ' + target_software.version)
        log_info('Image MD5......................: ' + target_software.md5_image)
        log_info('Install mode...................: ' + str(target_software.install_mode))
        if target_software.guestshell and target_software.md5_guestshell:
            log_info('Guest shell....................: ' + target_software.guestshell)
            log_info('Guest shell MD5................: ' + str(target_software.md5_guestshell))

        print('')
        log_info('Current ZTP status')
        update_status = False if device.current_version == target_software.version else True
        log_info('Update required................: ' + str(update_status))

        # switch_to_install_mode already done
        if device.install_mode and not update_status:
            _switch_to_install_mode = False
        else:
            _switch_to_install_mode = model.install_mode if model.install_mode is not None else switch_to_install_mode
            _switch_to_install_mode = target_software.install_mode if target_software.install_mode is not None else _switch_to_install_mode

        log_info('Switch to install mode required: ' + str(_switch_to_install_mode))

        log_info('Needs startup-config...........: ' + str(device.needs_startup))
        print('')

        # Cleanup any leftover install files, make space for this round
        device_cleanup()

        log_info('Flash size/free (MB)...........: ' + str(round(device.flash_size / 1024 / 1024)) + '/' +
                 str(round(device.get_flash_free() / 1024 / 1024)))

        # round 1: update
        if update_status:
            # check if image transfer needed
            if not check_file_exists(target_software.image):
                file_transfer(http_image, target_software.image, device.get_usb_present())

            # check if md5 correct
            if device.current_version[0:5] not in no_md5_verify:
                if not verify_md5(target_software.image, target_software.md5_image):
                    log_info('Attempting to (re)transfer image to device...')
                    file_transfer(http_image, target_software.image, device.get_usb_present())
                    if not verify_md5(target_software.image, target_software.md5_image):
                        log_critical('Failed transfer MD5 hash mismatch')
                        raise ValueError('Failed transfer')
                else:
                    pass

            # activate image
            if check_file_exists(target_software.image):
                log_info('Performing activate image ' + target_software.image + ' - device will reload')
                activate_image(target_software.image)
            # exit is update not finished
            sys.exit()
        else:
            pass

        # round 2: check if OS in install mode, if not change to install mode
        if _switch_to_install_mode:
            switch_to_install(target_software.image)
            sys.exit()

        # round 3: configure device
        if device.needs_startup:
            config_file = device.serial + '.cfg'
            log_info('Downloading config file: ' + config_file)
            file_transfer(http_config, config_file)
            log_info('Generate ssh key...')
            _configure('crypto key generate rsa modulus 4096 label ssh-key')
            _execute('write memory')
            log_info('Copy ' + config_file + ' to startup-config')
            _execute('copy ' + config_file + ' startup-config')
            _execute('delete /force flash:/' + config_file)
            log_info('System will reload in ' + str(reload_in) + ' minutes')
            _execute('reload in ' + str(reload_in))

        log_info('######  END OF ZTP SCRIPT ######')

    except Exception as e:
        log_critical('Failure encountered during day 0 provisioning.'
                     'Aborting ZTP script execution. Error details below')
        log_critical('Exception: ' + str(e))
        sys.exit(e)


def check_file_exists(file, file_system='flash:/'):
    dir_check = 'dir ' + file_system + file
    log_info('Checking to see if ' + file + ' exists on ' + file_system)
    results = cli(dir_check)
    if 'No such file or directory' in results:
        log_info('The ' + file + ' does NOT exist on ' + file_system)
        return False
    elif 'Directory of ' + file_system + file in results:
        log_info(file + ' DOES exist on ' + file_system)
        return True
    elif 'Directory of bootflash:/' + file in results:
        log_info(file + ' DOES exist on bootflash:/')
        return True
    else:
        log_critical('Unexpected output from check_file_exists')
        raise ValueError('Unexpected output from check_file_exists')


def device_cleanup():
    sleep_time_min = 3

    def __deploy_eem_cleanup_script():
        eem_commands = [
            'event manager applet cleanup',
            'event none maxrun ' + str(sleep_time_min * 60),
            'action 1.0 cli command "enable"',
            'action 2.0 cli command "install remove inactive" pattern "\[y\/n\]"',
            'action 2.1 cli command "y" pattern "proceed"',
            'action 2.2 cli command "y"',
            'action 3.1 cli command "delete /force flash:/downloaded_script.py"',
            'action 3.2 cli command "delete /force flash:/guest-share/downloaded_script.py"',
            'action 3.3 cli command "delete /force flash:/guest-share/ztp.py"',
            'action 4.0 cli command "delete /force flash:/core/*"',
            'action 4.1 cli command "delete /force flash:/tracelog/*"',
            'action 4.2 cli command "delete /force flash:/license_evlog/*"',
        ]
        _configure(eem_commands)

    def __remove_eem_cleanup_script():
        eem_commands = [
            'no event manager applet cleanup',
        ]
        _configure(eem_commands)

    __deploy_eem_cleanup_script()
    log_info('Running cleanup EEM Script')
    cli('event manager run cleanup')
    log_info('Wait ' + str(sleep_time_min) + ' minutes for cleanup to finish')
    sleep((sleep_time_min * 60) + 5)
    __remove_eem_cleanup_script()
    log_info('Finished cleanup EEM script')


def activate_image(image):
    _configure([
        'no boot system',
        'boot system flash ' + image,
    ])
    _execute('write memory')
    _execute('write erase')
    log_info('System will reload in ' + str(reload_in) + ' minutes')
    _execute('reload in ' + str(reload_in))


def switch_to_install(image):
    log_info('Performing switch to install mode - device will reload')
    sleep_time_min = 40
    _configure([
        'no boot system',
        'boot system flash packages.conf',
        # needs event manger, because you can not run "install add .." with _execute() :-(
        'event manager applet switch_to_install',
        ' event none maxrun ' + str(sleep_time_min * 60),
        ' action 1.0 cli command "enable"',
        ' action 2.0 cli command "install add file flash:/' + image + ' activate commit prompt-level none"',
    ])
    _execute('write memory')
    _execute('write erase')
    log_info('Wait up to ' + str(sleep_time_min) + ' minutes to get the change to install mode done...')
    _execute('event manager run switch_to_install')
    sleep((sleep_time_min * 60) + 5)
    log_info(
        'EEM switch to install mode took more than ' + str(sleep_time_min) +
        ' minutes.Increase the sleep time by few minutes before retrying'
    )


def file_transfer(http_server, file, usb=False):
    # check if file exist on usb, if so transfer from there
    if usb and check_file_exists(file, 'usb0:/'):
        log_info('File found on usb0, copy from there...')
        res = cli('copy usb0:/' + file + ' flash:/' + file)
    else:
        log_info('Start transferring ' + file + ' from http ' + http_server + '...')
        log_info('Depending on file size and transfer speed this can take some time (up to 1 hour or more)')
        res = cli('copy http://' + http_server + '/' + file + ' flash:/' + file)
    log_info(res)
    log_info('Finished transferring ' + file)


def verify_md5(image, src_md5, file_system='flash:/'):
    log_info('Verifying MD5 for ' + file_system + image)
    try:
        dst_md5 = cli('verify /md5 ' + file_system + image)
        if src_md5 in dst_md5:
            log_info('MD5 hashes match')
            return True
        else:
            log_critical('MD5 checksum mismatch')
            return False
    except Exception as e:
        log_info('MD5 checksum failed due to an exception')
        log_info('Exception: ' + str(e))
        return True  # why return True on error?


def create_logfile():
    try:
        print('Creating a persistent log file')
        path = '/flash/guest-share/ztp.log'
        with open(path, 'a+') as fp:
            pass
        return path
    except IOError:
        print('Couldnt create a log file at guest-share. Trying to use /flash/ztp.log as an alternate log path')
        path = '/flash/ztp.log'
        with open(path, 'a+') as fp:
            pass
        return path
    except Exception as e:
        print('Couldn\'t create a log file to proceed ' + str(e))


def configure_logger(path):
    log_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
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
    ztp_log = logging.getLogger('root')
    ztp_log.setLevel(logging.INFO)
    ztp_log.addHandler(log_handler)


def log_info(message):
    print(time.asctime() + ' :: INFO :: ' + message)
    if log_to_file:
        ztp_log = logging.getLogger('root')
        ztp_log.info(message)


def log_critical(message):
    print(time.asctime() + ' :: CRIT :: ' + message)
    if log_to_file:
        ztp_log = logging.getLogger('root')
        ztp_log.critical(message)


def sleep(sleep_time):
    log_info('going to sleep for ' + str(sleep_time) + ' seconds')
    time.sleep(sleep_time)


if __name__ == '__main__':
    main()
