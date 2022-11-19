```
ro01#pnpa service reset no-prompt

Nov 19 17:50:49.406: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as vty0
Nov 19 17:50:49.461: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as vty0
Nov 19 17:50:49.491: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as vty0
Nov 19 17:50:49.521: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as vty0
Nov 19 17:50:49.552: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as vty0
Nov 19 17:50:49.561: %CRYPTO_ENGINE-5-KEY_DELETED: A key named TP-self-signed-1007201388 has been removed from key storage
Nov 19 17:50:49.564: %CRYPTO_ENGINE-5-KEY_DELETED: A key named ssh-key has been removed from key storage
Nov 19 17:50:49.565: %CRYPTO_ENGINE-5-KEY_DELETED: A key named ssh-key.server has been removed from key storage
Nov 19 17:50:49.575: %SSH-5-DISABLED: SSH 2.0 has been disabled
Nov 19 17:50:49.592: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
Nov 19 17:50:50.613: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
Nov 19 17:50:51.617: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
Nov 19 17:50:52.616: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
Nov 19 17:51:05.131: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as consolePNP-RELOAD (1): status=[Reloading...], run-by=[pid=588, pname=Exec], log-name=[/pnp-info/pnp-reload-log] (log-size=0), reload-op=[reload-in], reload-with=[reload-erase-startup], reload-cancel=[No], reload-in-sec=30, user:[PnP reset CLI], reason:[PnP reset CLI], save-config=[No], do-reset=[No], erase-config=[Yes], err=0 [-], (elapsed-time=0 sec)
PNP-SERVICE-LOG (0): service log saved to [/pnp-info/pnp-reload-log] (377 bytes)
[
************************************************************************************************************
Erasing Nvram will not clear license trust code.
************************************************************************************************************
Nov 19 17:51:06.180: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
]
PNP-RELOAD (2): status=[Reload service OK], run-by=[pid=588, pname=Exec], log-name=[/pnp-info/pnp-reload-log] (log-size=377), reload-op=[reload-in], reload-with=[reload-erase-startup], reload-cancel=[No], reload-in-sec=30, user:[PnP reset CLI], reason:[PnP reset CLI], save-config=[No], do-reset=[No], erase-config=[Yes], err=0 [-], (elapsed-time=2 sec)
PnP reset is done. Device will reload soon
PnP reset is done
ro01#
Nov 19 17:51:08.983: %SYS-7-NV_BLOCK_INIT: Initialized the geometry of nvram
Nov 19 17:51:09.144: %PNP-6-PNP_SAVING_TECH_SUMMARY: Saving PnP tech summary (/pnp-tech/pnp-tech-reload-summary)... Please wait. Do not interrupt.
Nov 19 17:51:09.268: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
Nov 19 17:51:09.386: %PNP-6-PNP_SUDI_UPDATE: Device SUDI [PID:C1117-4PMLTEEAWE,SN:FGL223590FL] identified
Nov 19 17:51:09.699: %SYS-5-CONFIG_P: Configured programmatically by process Exec from console as console
ro01#
Nov 19 17:51:09.803: %PNP-6-PNP_TECH_SUMMARY_SAVED_OK: PnP tech summary (/pnp-tech/pnp-tech-reload-summary) saved successfully (elapsed time: 1 seconds).
Nov 19 17:51:09.804: %PNP-6-PNP_RESET_DONE: PnP reset done
ro01#


***
*** --- SHUTDOWN NOW ---
***

ro01#
Nov 19 17:51:41.586: %SYS-5-RELOAD: Reload requested by PnP reset CLI. Reload Reason: PnP reset CLI.
ro01#
Rom image verified correctly


System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


........

Located packages.conf
#

######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

Package header rev 3 structure detected
IsoSize = 0
Performing Integrity Check ...
Performing Signature Verification ...
RSA Signed RELEASE Image Signature Verification Successful
Image validated


              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           Cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco IOS Software [Bengaluru], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.3a, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Fri 08-Apr-22 12:42 by mcpre


This software version supports only Smart Licensing as the software licensing mechanism.


PLEASE READ THE FOLLOWING TERMS CAREFULLY. INSTALLING THE LICENSE OR
LICENSE KEY PROVIDED FOR ANY CISCO SOFTWARE PRODUCT, PRODUCT FEATURE,
AND/OR SUBSEQUENTLY PROVIDED SOFTWARE FEATURES (COLLECTIVELY, THE
"SOFTWARE"), AND/OR USING SUCH SOFTWARE CONSTITUTES YOUR FULL
ACCEPTANCE OF THE FOLLOWING TERMS. YOU MUST NOT PROCEED FURTHER IF YOU
ARE NOT WILLING TO BE BOUND BY ALL THE TERMS SET FORTH HEREIN.

Your use of the Software is subject to the Cisco End User License Agreement
(EULA) and any relevant supplemental terms (SEULA) found at
http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html.

You hereby acknowledge and agree that certain Software and/or features are
licensed for a particular term, that the license to such Software and/or
features is valid only for the applicable term and that such Software and/or
features may be shut down or otherwise terminated by Cisco after expiration
of the applicable license term (e.g., 90-day trial period). Cisco reserves
the right to terminate any such Software feature electronically or by any
other means available. While Cisco may provide alerts, it is your sole
responsibility to monitor your usage of any such term Software feature to
ensure that your systems and networks are prepared for a shutdown of the
Software feature.


% Failed to initialize nvram
% Failed to initialize backup nvram

All TCP AO KDF Tests Pass
cisco C1117-4PMLTEEAWE (1RU) processor with 1398054K/6147K bytes of memory.
Processor board ID FGL223590FL
Router operating mode: Autonomous
1 Ethernet interface
1 Virtual Ethernet interface
6 Gigabit Ethernet interfaces
1 ATM interface
2 Cellular interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
2863103K bytes of flash memory at bootflash:.

 WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
No startup-config, starting autoinstall/pnp/ztp...

Autoinstall will terminate if any input is detected on console

Autoinstall trying DHCPv4 on GigabitEthernet0/0/0

Autoinstall trying DHCPv6 on GigabitEthernet0/0/0



         --- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]:
Acquired IPv4 address 10.10.10.48 on Interface GigabitEthernet0/0/0
Received following DHCPv4 options:
        domain-name     : home.intern
        bootfile        : http://192.168.10.15/ztp.py

stop Autoip processFailed to generate persistent self-signed certificate.
    Secure server will use temporary self-signed certificate.

OK to enter CLI now...

pnp-discovery can be monitored without entering enable mode

Entering enable mode will stop pnp-discovery

Attempting bootfile http://192.168.10.15/ztp.py

Loading http://192.168.10.15/ztp.py
Loading http://192.168.10.15/ztp.py
                                    %FLASH_CHECK-3-DISK_QUOTA: R0/0: flash_check: Flash disk quota exceeded [free space is 794180 kB] - Please clean up files on bootflash.
                           day0guestshell activated successfully
Current state is: ACTIVATED
day0guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully
Creating a persistent log file
Log file created in : /flash/guest-share/ztp.log
Sat Nov 19 13:48:44 2022 :: INFO :: ###### STARTING ZTP SCRIPT ######

Sat Nov 19 13:48:44 2022 :: INFO :: Getting device info
Sat Nov 19 13:48:46 2022 :: INFO :: Model..........................: C1117-4PMLTEEAWE
Sat Nov 19 13:48:46 2022 :: INFO :: Serial number..................: FGL223590FL
Sat Nov 19 13:48:46 2022 :: INFO :: Current version................: 17.06.03a
Sat Nov 19 13:48:46 2022 :: INFO :: Install mode...................: False
Sat Nov 19 13:48:46 2022 :: INFO :: Flash size/free (MB)...........: 2774/193
Sat Nov 19 13:48:46 2022 :: INFO :: USB present....................: False

Sat Nov 19 13:48:46 2022 :: INFO :: Target image data
Sat Nov 19 13:48:46 2022 :: INFO :: Image..........................: c1100-universalk9.17.06.04.SPA.bin
Sat Nov 19 13:48:46 2022 :: INFO :: Version........................: 17.06.04
Sat Nov 19 13:48:46 2022 :: INFO :: Image MD5......................: 2caa962f5ed0ecc52f99b90c733c54de
Sat Nov 19 13:48:46 2022 :: INFO :: Install mode...................: True

Sat Nov 19 13:48:46 2022 :: INFO :: Current ZTP status
Sat Nov 19 13:48:46 2022 :: INFO :: Update required................: True
Sat Nov 19 13:48:46 2022 :: INFO :: Switch to install mode required: True
Sat Nov 19 13:48:46 2022 :: INFO :: Needs startup-config...........: True

Sat Nov 19 13:48:46 2022 :: INFO :: Running cleanup EEM Script
Sat Nov 19 13:49:17 2022 :: INFO :: Wait 3 minutes for cleanup to finish
Sat Nov 19 13:49:17 2022 :: INFO :: going to sleep for 185 seconds
Sat Nov 19 13:52:22 2022 :: INFO :: Finished cleanup EEM script
Sat Nov 19 13:52:22 2022 :: INFO :: Flash size/free (MB)...........: 2774/922
Sat Nov 19 13:52:22 2022 :: INFO :: Checking to see if c1100-universalk9.17.06.04.SPA.bin exists on flash:/
Sat Nov 19 13:52:22 2022 :: INFO :: The c1100-universalk9.17.06.04.SPA.bin does NOT exist on flash:/
Sat Nov 19 13:52:23 2022 :: INFO :: Start transferring c1100-universalk9.17.06.04.SPA.bin from http 192.168.10.15...
Sat Nov 19 13:52:23 2022 :: INFO :: Depending on file size and transfer speed this can take some time (up to 1 hour or more)
Sat Nov 19 14:11:55 2022 :: INFO :: Accessing http://192.168.10.15/c1100-universalk9.17.06.04.SPA.bin...
Loading http://192.168.10.15/c1100-universalk9.17.06.04.SPA.bin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
706565772 bytes copied in 1171.344 secs (603209 bytes/sec)

Sat Nov 19 14:11:55 2022 :: INFO :: Finished transferring c1100-universalk9.17.06.04.SPA.bin
Sat Nov 19 14:11:55 2022 :: INFO :: Verifying MD5 for flash:/c1100-universalk9.17.06.04.SPA.bin
Sat Nov 19 14:12:20 2022 :: INFO :: MD5 hashes match
Sat Nov 19 14:12:20 2022 :: INFO :: Checking to see if c1100-universalk9.17.06.04.SPA.bin exists on flash:/
Sat Nov 19 14:12:20 2022 :: INFO :: c1100-universalk9.17.06.04.SPA.bin DOES exist on bootflash:/
Sat Nov 19 14:12:20 2022 :: INFO :: Performing activate image c1100-universalk9.17.06.04.SPA.bin - device will reload
Building configuration...
[OK]

************************************************************************************************************
Erasing Nvram will not clear license trust code.
************************************************************************************************************
Erasing the nvram filesystem will remove all configuration files! Continue? [OK]
Erase of nvram: complete

Sat Nov 19 14:12:33 2022 :: INFO :: System will reload in 2 minutes
Reload scheduled for 14:14:33 UTC Sat Nov 19 2022 (in 2 minutes) by ZTP on vty72
Reload reason: Reload Command


Guestshell destroyed successfully
Script execution success!



Press RETURN to get started!


stop Autoip process
Nov 19 14:13:14.539: %SYS-5-USERLOG_NOTICE: Message from tty0(user id: ): Device in day0 workflow, some non user-configured options may be enabled by default
Nov 19 14:13:14.696: %SYS-5-CONFIG_P: Configured programmatically by process DHCP Autoinstall from console as vty0
Nov 19 14:13:15.637: %LINK-5-CHANGED: Interface VirtualPortGroup31, changed state to administratively down
Nov 19 14:13:16.637: %LINEPROTO-5-UPDOWN: Line protocol on Interface VirtualPortGroup31, changed state to down
Nov 19 14:13:25.083: %PLATFORM-5-LOWSPACERECOVER:  bootflash : low space alarm deassert


***
*** --- SHUTDOWN in 0:01:00 ---
***



***
*** --- SHUTDOWN NOW ---
***

Nov 19 14:14:36.222: %SYS-5-RELOAD: Reload requested by ZTP on vty72. Reload Reason: Reload Command.Rom image verified correctly


System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


......

Located c1100-universalk9.17.06.04.SPA.bin
#####################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

Package header rev 3 structure detected
IsoSize = 648642560
Performing Integrity Check ...
Performing Signature Verification ...
RSA Signed RELEASE Image Signature Verification Successful
Image validated


              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           Cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco IOS Software [Bengaluru], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Sun 14-Aug-22 08:10 by mcpre


This software version supports only Smart Licensing as the software licensing mechanism.


PLEASE READ THE FOLLOWING TERMS CAREFULLY. INSTALLING THE LICENSE OR
LICENSE KEY PROVIDED FOR ANY CISCO SOFTWARE PRODUCT, PRODUCT FEATURE,
AND/OR SUBSEQUENTLY PROVIDED SOFTWARE FEATURES (COLLECTIVELY, THE
"SOFTWARE"), AND/OR USING SUCH SOFTWARE CONSTITUTES YOUR FULL
ACCEPTANCE OF THE FOLLOWING TERMS. YOU MUST NOT PROCEED FURTHER IF YOU
ARE NOT WILLING TO BE BOUND BY ALL THE TERMS SET FORTH HEREIN.

Your use of the Software is subject to the Cisco End User License Agreement
(EULA) and any relevant supplemental terms (SEULA) found at
http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html.

You hereby acknowledge and agree that certain Software and/or features are
licensed for a particular term, that the license to such Software and/or
features is valid only for the applicable term and that such Software and/or
features may be shut down or otherwise terminated by Cisco after expiration
of the applicable license term (e.g., 90-day trial period). Cisco reserves
the right to terminate any such Software feature electronically or by any
other means available. While Cisco may provide alerts, it is your sole
responsibility to monitor your usage of any such term Software feature to
ensure that your systems and networks are prepared for a shutdown of the
Software feature.


% Failed to initialize nvram
% Failed to initialize backup nvram

All TCP AO KDF Tests Pass
cisco C1117-4PMLTEEAWE (1RU) processor with 1397937K/6147K bytes of memory.
Processor board ID FGL223590FL
Router operating mode: Autonomous
1 Ethernet interface
1 Virtual Ethernet interface
6 Gigabit Ethernet interfaces
1 ATM interface
2 Cellular interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
2863103K bytes of flash memory at bootflash:.

 WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
No startup-config, starting autoinstall/pnp/ztp...

Autoinstall will terminate if any input is detected on console

Autoinstall trying DHCPv4 on GigabitEthernet0/0/0

Autoinstall trying DHCPv6 on GigabitEthernet0/0/0



         --- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]:
Acquired IPv4 address 10.10.10.49 on Interface GigabitEthernet0/0/0
Received following DHCPv4 options:
        domain-name     : home.intern
        bootfile        : http://192.168.10.15/ztp.py

stop Autoip processFailed to generate persistent self-signed certificate.
    Secure server will use temporary self-signed certificate.

OK to enter CLI now...

pnp-discovery can be monitored without entering enable mode

Entering enable mode will stop pnp-discovery

Attempting bootfile http://192.168.10.15/ztp.py

Loading http://192.168.10.15/ztp.py
Loading http://192.168.10.15/ztp.py
                                    %FLASH_CHECK-3-DISK_QUOTA: R0/0: flash_check: Flash disk quota exceeded [free space is 931904 kB] - Please clean up files on bootflash.
                           day0guestshell activated successfully
Current state is: ACTIVATED
day0guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully
Creating a persistent log file
Log file created in : /flash/guest-share/ztp.log
Sat Nov 19 14:22:25 2022 :: INFO :: ###### STARTING ZTP SCRIPT ######

Sat Nov 19 14:22:25 2022 :: INFO :: Getting device info
Sat Nov 19 14:22:26 2022 :: INFO :: Model..........................: C1117-4PMLTEEAWE
Sat Nov 19 14:22:26 2022 :: INFO :: Serial number..................: FGL223590FL
Sat Nov 19 14:22:26 2022 :: INFO :: Current version................: 17.06.04
Sat Nov 19 14:22:26 2022 :: INFO :: Install mode...................: False
Sat Nov 19 14:22:26 2022 :: INFO :: Flash size/free (MB)...........: 2774/248
Sat Nov 19 14:22:26 2022 :: INFO :: USB present....................: False

Sat Nov 19 14:22:26 2022 :: INFO :: Target image data
Sat Nov 19 14:22:26 2022 :: INFO :: Image..........................: c1100-universalk9.17.06.04.SPA.bin
Sat Nov 19 14:22:26 2022 :: INFO :: Version........................: 17.06.04
Sat Nov 19 14:22:26 2022 :: INFO :: Image MD5......................: 2caa962f5ed0ecc52f99b90c733c54de
Sat Nov 19 14:22:26 2022 :: INFO :: Install mode...................: True

Sat Nov 19 14:22:26 2022 :: INFO :: Current ZTP status
Sat Nov 19 14:22:26 2022 :: INFO :: Update required................: False
Sat Nov 19 14:22:26 2022 :: INFO :: Switch to install mode required: True
Sat Nov 19 14:22:26 2022 :: INFO :: Needs startup-config...........: True

Sat Nov 19 14:22:27 2022 :: INFO :: Running cleanup EEM Script
Sat Nov 19 14:22:58 2022 :: INFO :: Wait 3 minutes for cleanup to finish
Sat Nov 19 14:22:58 2022 :: INFO :: going to sleep for 185 seconds
Sat Nov 19 14:26:03 2022 :: INFO :: Finished cleanup EEM script
Sat Nov 19 14:26:03 2022 :: INFO :: Flash size/free (MB)...........: 2774/921
Sat Nov 19 14:26:03 2022 :: INFO :: Performing switch to install mode - device will reload
Building configuration...
[OK]

************************************************************************************************************
Erasing Nvram will not clear license trust code.
************************************************************************************************************
Erasing the nvram filesystem will remove all configuration files! Continue? [OK]
Erase of nvram: complete

Sat Nov 19 14:26:16 2022 :: INFO :: Wait up to 40 minutes to get the change to install mode done...
Sat Nov 19 14:26:46 2022 :: INFO :: going to sleep for 2405 seconds
Rom image verified correctly


System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


........

Located packages.conf
#

######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

Package header rev 3 structure detected
IsoSize = 0
Performing Integrity Check ...
Performing Signature Verification ...
RSA Signed RELEASE Image Signature Verification Successful
Image validated


%FLASH_CHECK-3-DISK_QUOTA: R0/0: flash_check: Flash disk quota exceeded [free space is 195940 kB] - Please clean up files on bootflash.

              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           Cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco IOS Software [Bengaluru], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Sun 14-Aug-22 08:10 by mcpre


This software version supports only Smart Licensing as the software licensing mechanism.


PLEASE READ THE FOLLOWING TERMS CAREFULLY. INSTALLING THE LICENSE OR
LICENSE KEY PROVIDED FOR ANY CISCO SOFTWARE PRODUCT, PRODUCT FEATURE,
AND/OR SUBSEQUENTLY PROVIDED SOFTWARE FEATURES (COLLECTIVELY, THE
"SOFTWARE"), AND/OR USING SUCH SOFTWARE CONSTITUTES YOUR FULL
ACCEPTANCE OF THE FOLLOWING TERMS. YOU MUST NOT PROCEED FURTHER IF YOU
ARE NOT WILLING TO BE BOUND BY ALL THE TERMS SET FORTH HEREIN.

Your use of the Software is subject to the Cisco End User License Agreement
(EULA) and any relevant supplemental terms (SEULA) found at
http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html.

You hereby acknowledge and agree that certain Software and/or features are
licensed for a particular term, that the license to such Software and/or
features is valid only for the applicable term and that such Software and/or
features may be shut down or otherwise terminated by Cisco after expiration
of the applicable license term (e.g., 90-day trial period). Cisco reserves
the right to terminate any such Software feature electronically or by any
other means available. While Cisco may provide alerts, it is your sole
responsibility to monitor your usage of any such term Software feature to
ensure that your systems and networks are prepared for a shutdown of the
Software feature.


% Failed to initialize nvram
% Failed to initialize backup nvram

All TCP AO KDF Tests Pass
cisco C1117-4PMLTEEAWE (1RU) processor with 1397937K/6147K bytes of memory.
Processor board ID FGL223590FL
Router operating mode: Autonomous
1 Ethernet interface
1 Virtual Ethernet interface
6 Gigabit Ethernet interfaces
1 ATM interface
2 Cellular interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
2863103K bytes of flash memory at bootflash:.

 WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
No startup-config, starting autoinstall/pnp/ztp...

Autoinstall will terminate if any input is detected on console

Autoinstall trying DHCPv4 on GigabitEthernet0/0/0

Autoinstall trying DHCPv6 on GigabitEthernet0/0/0



         --- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]:
Acquired IPv4 address 10.10.10.49 on Interface GigabitEthernet0/0/0
Received following DHCPv4 options:
        domain-name     : home.intern
        bootfile        : http://192.168.10.15/ztp.py

stop Autoip processFailed to generate persistent self-signed certificate.
    Secure server will use temporary self-signed certificate.

OK to enter CLI now...

pnp-discovery can be monitored without entering enable mode

Entering enable mode will stop pnp-discovery

Attempting bootfile http://192.168.10.15/ztp.py

Loading http://192.168.10.15/ztp.py
Loading http://192.168.10.15/ztp.py day0guestshell activated successfully
Current state is: ACTIVATED
day0guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully
Creating a persistent log file
Log file created in : /flash/guest-share/ztp.log
Sat Nov 19 14:43:59 2022 :: INFO :: ###### STARTING ZTP SCRIPT ######

Sat Nov 19 14:43:59 2022 :: INFO :: Getting device info
Sat Nov 19 14:44:00 2022 :: INFO :: Model..........................: C1117-4PMLTEEAWE
Sat Nov 19 14:44:00 2022 :: INFO :: Serial number..................: FGL223590FL
Sat Nov 19 14:44:00 2022 :: INFO :: Current version................: 17.06.04
Sat Nov 19 14:44:00 2022 :: INFO :: Install mode...................: True
Sat Nov 19 14:44:00 2022 :: INFO :: Flash size/free (MB)...........: 2774/192
Sat Nov 19 14:44:00 2022 :: INFO :: USB present....................: False

Sat Nov 19 14:44:00 2022 :: INFO :: Target image data
Sat Nov 19 14:44:00 2022 :: INFO :: Image..........................: c1100-universalk9.17.06.04.SPA.bin
Sat Nov 19 14:44:00 2022 :: INFO :: Version........................: 17.06.04
Sat Nov 19 14:44:00 2022 :: INFO :: Image MD5......................: 2caa962f5ed0ecc52f99b90c733c54de
Sat Nov 19 14:44:00 2022 :: INFO :: Install mode...................: True

Sat Nov 19 14:44:00 2022 :: INFO :: Current ZTP status
Sat Nov 19 14:44:00 2022 :: INFO :: Update required................: False
Sat Nov 19 14:44:00 2022 :: INFO :: Switch to install mode required: False
Sat Nov 19 14:44:00 2022 :: INFO :: Needs startup-config...........: True

Sat Nov 19 14:44:00 2022 :: INFO :: Running cleanup EEM Script
Sat Nov 19 14:44:31 2022 :: INFO :: Wait 3 minutes for cleanup to finish
Sat Nov 19 14:44:31 2022 :: INFO :: going to sleep for 185 seconds
Sat Nov 19 14:47:36 2022 :: INFO :: Finished cleanup EEM script
Sat Nov 19 14:47:36 2022 :: INFO :: Flash size/free (MB)...........: 2774/865
Sat Nov 19 14:47:36 2022 :: INFO :: Downloading config file: FGL223590FL.cfg
Sat Nov 19 14:47:36 2022 :: INFO :: Start transferring FGL223590FL.cfg from http 192.168.10.15...
Sat Nov 19 14:47:36 2022 :: INFO :: Depending on file size and transfer speed this can take some time (up to 1 hour or more)
Sat Nov 19 14:47:36 2022 :: INFO :: Accessing http://192.168.10.15/FGL223590FL.cfg...
Loading http://192.168.10.15/FGL223590FL.cfg
1613 bytes copied in 0.028 secs (57607 bytes/sec)

Sat Nov 19 14:47:36 2022 :: INFO :: Finished transferring FGL223590FL.cfg
Sat Nov 19 14:47:36 2022 :: INFO :: Generate ssh key...
Building configuration...
[OK]

Sat Nov 19 14:48:14 2022 :: INFO :: Copy FGL223590FL.cfg to startup-config
1613 bytes copied in 3.692 secs (437 bytes/sec)

Sat Nov 19 14:48:18 2022 :: INFO :: System will reload in 2 minutes
Reload scheduled for 14:50:19 UTC Sat Nov 19 2022 (in 2 minutes) by ZTP on vty72
Reload reason: Reload Command

Sat Nov 19 14:48:19 2022 :: INFO :: ######  END OF ZTP SCRIPT ######

Guestshell destroyed successfully
Script execution success!



Press RETURN to get started!


stop Autoip process
Nov 19 14:49:00.241: %SYS-5-USERLOG_NOTICE: Message from tty0(user id: ): Device in day0 workflow, some non user-configured options may be enabled by default
Nov 19 14:49:00.306: %SYS-5-CONFIG_P: Configured programmatically by process DHCP Autoinstall from console as vty0
Nov 19 14:49:01.392: %LINK-5-CHANGED: Interface VirtualPortGroup31, changed state to administratively down
Nov 19 14:49:02.393: %LINEPROTO-5-UPDOWN: Line protocol on Interface VirtualPortGroup31, changed state to down


***
*** --- SHUTDOWN in 0:01:00 ---
***



***
*** --- SHUTDOWN NOW ---
***

Nov 19 14:50:21.233: %SYS-5-RELOAD: Reload requested by ZTP on vty72. Reload Reason: Reload Command.Rom image verified correctly


System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


........

Located packages.conf
#

######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

Package header rev 3 structure detected
IsoSize = 0
Performing Integrity Check ...
Performing Signature Verification ...
RSA Signed RELEASE Image Signature Verification Successful
Image validated


              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           Cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco IOS Software [Bengaluru], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Sun 14-Aug-22 08:10 by mcpre


This software version supports only Smart Licensing as the software licensing mechanism.


PLEASE READ THE FOLLOWING TERMS CAREFULLY. INSTALLING THE LICENSE OR
LICENSE KEY PROVIDED FOR ANY CISCO SOFTWARE PRODUCT, PRODUCT FEATURE,
AND/OR SUBSEQUENTLY PROVIDED SOFTWARE FEATURES (COLLECTIVELY, THE
"SOFTWARE"), AND/OR USING SUCH SOFTWARE CONSTITUTES YOUR FULL
ACCEPTANCE OF THE FOLLOWING TERMS. YOU MUST NOT PROCEED FURTHER IF YOU
ARE NOT WILLING TO BE BOUND BY ALL THE TERMS SET FORTH HEREIN.

Your use of the Software is subject to the Cisco End User License Agreement
(EULA) and any relevant supplemental terms (SEULA) found at
http://www.cisco.com/c/en/us/about/legal/cloud-and-software/software-terms.html.

You hereby acknowledge and agree that certain Software and/or features are
licensed for a particular term, that the license to such Software and/or
features is valid only for the applicable term and that such Software and/or
features may be shut down or otherwise terminated by Cisco after expiration
of the applicable license term (e.g., 90-day trial period). Cisco reserves
the right to terminate any such Software feature electronically or by any
other means available. While Cisco may provide alerts, it is your sole
responsibility to monitor your usage of any such term Software feature to
ensure that your systems and networks are prepared for a shutdown of the
Software feature.



All TCP AO KDF Tests Pass
cisco C1117-4PMLTEEAWE (1RU) processor with 1397937K/6147K bytes of memory.
Processor board ID FGL223590FL
Router operating mode: Autonomous
1 Ethernet interface
1 Virtual Ethernet interface
6 Gigabit Ethernet interfaces
1 ATM interface
2 Cellular interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
2863103K bytes of flash memory at bootflash:.

 WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
SETUP: new interface Cellular0/2/0 placed in "shutdown" state
SETUP: new interface Cellular0/2/1 placed in "shutdown" state
SETUP: new interface ATM0/3/0 placed in "shutdown" state
SETUP: new interface Ethernet0/3/0 placed in "shutdown" state


Press RETURN to get started!


*Nov 19 14:53:03.800: %ISR_THROUGHPUT-6-CRYPTO: Crypto level has been set to 50000 kbps
*Nov 19 14:53:07.300: %SMART_LIC-6-AGENT_ENABLED: Smart Agent for Licensing is enabled
*Nov 19 14:53:07.710: %SMART_LIC-6-EXPORT_CONTROLLED: Usage of export controlled features is not allowedESG-PM-ACL:[subsys-init] Init ESG-ACL subsystem starting

*Nov 19 14:53:10.271: ESG-PM-ACL:[subsys-init] Init ESG-ACL platform API reg

*Nov 19 14:53:10.272: ESG-PM-ACL:[subsys-init] Init ESG-ACL subsystem ended

*Nov 19 14:53:10.272:
*Nov 19 14:53:15.981: %SPANTREE-5-EXTENDED_SYSID: Extended SysId enabled for type vlan
*Nov 19 14:53:16.095: %TLSCLIENT-5-TLSCLIENT_IOS: TLS Client is IOS based
*Nov 19 14:53:16.432: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_ENFORCED: Cisco PSB security compliance is being enforced
*Nov 19 14:53:16.432: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by this platform for use of RSA Key Size
*Nov 19 14:53:16.616: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKEv2 for use of DES
*Nov 19 14:53:16.617: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKEv2 for use of 3DES
*Nov 19 14:53:16.617: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKEv2 for use of DH
*Nov 19 14:53:16.617: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKEv2 for use of MD5
*Nov 19 14:53:16.617: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKEv2 for use of SHA1
*Nov 19 14:53:16.629: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKMP for use of DES
*Nov 19 14:53:16.629: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKMP for use of 3DES
*Nov 19 14:53:16.629: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKMP for use of DH
*Nov 19 14:53:16.629: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKMP for use of MD5
*Nov 19 14:53:16.629: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by Crypto IKMP for use of SHA1
*Nov 19 14:53:16.633: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by IPSEC key engine for use of 3DES
*Nov 19 14:53:16.633: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by IPSEC key engine for use of MD5
*Nov 19 14:53:16.633: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by IPSEC key engine for use of DES
*Nov 19 14:53:17.598: %LINK-3-UPDOWN: Interface Lsmpi0, changed state to up
*Nov 19 14:53:17.635: %LINK-3-UPDOWN: Interface EOBC0, changed state to up
*Nov 19 14:53:17.638: %LINEPROTO-5-UPDOWN: Line protocol on Interface LI-Null0, changed state to up
*Nov 19 14:53:17.640: %LINK-3-UPDOWN: Interface LIIN0, changed state to up
*Nov 19 14:53:17.772: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by encrypt proc for use of 3DES
*Nov 19 14:53:17.772: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by encrypt proc for use of MD5
*Nov 19 14:53:17.772: %CRYPTO_ENGINE-5-CSDL_COMPLIANCE_EXCEPTION_ADDED: Cisco PSB security compliance exception has been added by encrypt proc for use of DES
*Nov 19 14:53:17.844: %PNP-6-PNP_DISCOVERY_STARTED: PnP Discovery started
*Nov 19 14:52:18.022: %BOOT-5-OPMODE_LOG: R0/0: binos: System booted in AUTONOMOUS mode
*Nov 19 14:53:07.300: %CMLIB-6-THROUGHPUT_VALUE: R0/0: cmand: Throughput license found, throughput set to 50000 kbps
*Nov 19 14:53:19.620: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan1, changed state to down
*Nov 19 14:53:19.621: %LINEPROTO-5-UPDOWN: Line protocol on Interface Lsmpi0, changed state to up
*Nov 19 14:53:19.623: %LINEPROTO-5-UPDOWN: Line protocol on Interface EOBC0, changed state to up
*Nov 19 14:53:19.625: %LINEPROTO-5-UPDOWN: Line protocol on Interface LIIN0, changed state to up
*Nov 19 14:53:21.456: %ONEP_BASE-6-SS_ENABLED: ONEP: Service set Base was enabled by Default
*Nov 19 14:53:25.750: %SYS-7-NVRAM_INIT_WAIT_TIME: Waited 0 seconds for NVRAM to be available
*Nov 19 14:53:26.572: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named TP-self-signed-1007201388 has been generated or imported by crypto config
*Nov 19 14:53:26.614: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named ssh-key has been generated or imported by crypto config
*Nov 19 14:53:26.638: %SYS-6-PRIVCFG_DECRYPT_SUCCESS: Successfully apply the private config file
*Nov 19 14:53:26.755: %AAAA-4-CLI_DEPRECATED: WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
*Nov 19 14:53:26.848: %SSH-5-DISABLED: SSH 1.99 has been disabled
*Nov 19 14:53:26.874: %SYS-6-CLOCKUPDATE: System clock has been updated from 14:53:26 UTC Sat Nov 19 2022 to 15:53:26 CET Sat Nov 19 2022, configured from console by vty0.
*Nov 19 14:53:26.878: %SYS-6-CLOCKUPDATE: System clock has been updated from 15:53:26 CET Sat Nov 19 2022 to 15:53:26 CET Sat Nov 19 2022, configured from console by vty0.
*Nov 19 14:53:26.902: get_spa_plugin_from_hwidb: spa ds is NULL in VirtualPortGroup0
*Nov 19 14:53:27.257: %SYS-5-CONFIG_I: Configured from memory by console
*Nov 19 14:53:27.344: %IOSXE_OIR-6-REMSPA: SPA removed from subslot 0/0, interfaces disabled
*Nov 19 14:53:27.347: %IOSXE_OIR-6-REMSPA: SPA removed from subslot 0/1, interfaces disabled
*Nov 19 14:53:27.348: %IOSXE_OIR-6-REMSPA: SPA removed from subslot 0/2, interfaces disabled
*Nov 19 14:53:27.348: %IOSXE_OIR-6-REMSPA: SPA removed from subslot 0/3, interfaces disabled
*Nov 19 14:53:27.348: %IOSXE_OIR-6-REMSPA: SPA removed from subslot 0/4, interfaces disabled
*Nov 19 14:53:27.366: %SPA_OIR-6-OFFLINECARD: SPA (C1117-1x1GE) offline in subslot 0/0
*Nov 19 14:53:27.381: %SPA_OIR-6-OFFLINECARD: SPA (C1117-ES-4) offline in subslot 0/1
*Nov 19 14:53:27.385: %CELLWAN-2-MODEM_DOWN: Modem in slot 0/2 is DOWN
*Nov 19 14:53:27.386: %CELLWAN-2-MODEM_DOWN: Modem in slot 0/2 is DOWN
*Nov 19 14:53:27.389: %SPA_OIR-6-OFFLINECARD: SPA (C1117-LTE) offline in subslot 0/2
*Nov 19 14:53:27.395: %SPA_OIR-6-OFFLINECARD: SPA (C1117-VADSL-M) offline in subslot 0/3
*Nov 19 14:53:27.396: %SPA_OIR-6-OFFLINECARD: SPA (ISR-AP1100AC-E) offline in subslot 0/4
*Nov 19 14:53:27.502: %IOSXE_OIR-6-INSCARD: Card (fp) inserted in slot F0
*Nov 19 14:53:27.502: %IOSXE_OIR-6-ONLINECARD: Card (fp) online in slot F0
*Nov 19 14:53:27.581: %IOSXE_OIR-6-INSCARD: Card (cc) inserted in slot 0
*Nov 19 14:53:27.581: %IOSXE_OIR-6-ONLINECARD: Card (cc) online in slot 0
*Nov 19 14:53:27.950: %IOSXE_OIR-6-INSSPA: SPA inserted in subslot 0/0
*Nov 19 14:53:27.951: %IOSXE_OIR-6-INSSPA: SPA inserted in subslot 0/1
*Nov 19 14:53:27.951: %IOSXE_OIR-6-INSSPA: SPA inserted in subslot 0/2
*Nov 19 14:53:27.951: %IOSXE_OIR-6-INSSPA: SPA inserted in subslot 0/3
*Nov 19 14:53:27.952: %IOSXE_OIR-6-INSSPA: SPA inserted in subslot 0/4
*Nov 19 14:53:27.572: %UICFGEXP-6-SERVER_NOTIFIED_START: R0/0: psd: Server iox has been notified to start
*Nov 19 14:53:29.925: %LINEPROTO-5-UPDOWN: Line protocol on Interface VirtualPortGroup0, changed state to up
*Nov 19 14:53:31.105: %SSH-5-ENABLED: SSH 2.0 has been enabled
*Nov 19 14:53:31.210: %CRYPTO-6-ISAKMP_ON_OFF: ISAKMP is OFF
*Nov 19 14:53:31.210: %CRYPTO-6-GDOI_ON_OFF: GDOI is OFF
*Nov 19 14:53:31.912: %SYS-5-RESTART: System restarted --
Cisco IOS Software [Bengaluru], ISR Software (ARMV8EL_LINUX_IOSD-UNIVERSALK9-M), Version 17.6.4, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Sun 14-Aug-22 08:10 by mcpre
*Nov 19 14:53:32.920: spa in 0/0, still in booting

*Nov 19 14:53:33.220: %LINK-3-UPDOWN: Interface GigabitEthernet0/1/0, changed state to down
*Nov 19 14:53:33.223: %LINK-3-UPDOWN: Interface GigabitEthernet0/1/1, changed state to down
*Nov 19 14:53:33.226: %LINK-3-UPDOWN: Interface GigabitEthernet0/1/2, changed state to down
*Nov 19 14:53:33.230: %LINK-3-UPDOWN: Interface GigabitEthernet0/1/3, changed state to down
*Nov 19 14:53:33.236: %LINK-3-UPDOWN: Interface Wlan-GigabitEthernet0/1/4, changed state to down
*Nov 19 14:53:34.228: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/0, changed state to down
*Nov 19 14:53:34.229: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/1, changed state to down
*Nov 19 14:53:34.229: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/2, changed state to down
*Nov 19 14:53:34.230: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/3, changed state to down
*Nov 19 14:53:34.244: %LINEPROTO-5-UPDOWN: Line protocol on Interface Wlan-GigabitEthernet0/1/4, changed state to down
*Nov 19 14:53:36.119: %SPA_OIR-6-ONLINECARD: SPA (C1117-1x1GE) online in subslot 0/0
*Nov 19 14:53:36.710: %CRYPTO-6-ISAKMP_ON_OFF: ISAKMP is OFF
*Nov 19 14:53:36.710: %CRYPTO-6-GDOI_ON_OFF: GDOI is OFF
*Nov 19 14:53:37.156: %PNP-6-PNP_BEST_UDI_UPDATE: Best UDI [PID:C1117-4PMLTEEAWE,VID:V01,SN:FGL223590FL] identified via (entity-mibs)
*Nov 19 14:53:37.156: %PNP-6-PNP_CDP_UPDATE: Device UDI [PID:C1117-4PMLTEEAWE,VID:V01,SN:FGL223590FL] identified for CDP
*Nov 19 14:53:37.157: %PNP-6-PNP_DISCOVERY_STOPPED: PnP Discovery stopped (Startup Config Present)
*Nov 19 14:53:37.740: %SYS-5-CONFIG_P: Configured programmatically by process EPM CREATE DEFAULT CWA URL ACL from console as console
*Nov 19 14:53:37.818: %SPA_OIR-6-ONLINECARD: SPA (C1117-ES-4) online in subslot 0/1
*Nov 19 14:53:38.016: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/0, changed state to down
*Nov 19 14:53:38.080: %PKI-6-TRUSTPOINT_CREATE: Trustpoint: CISCO_IDEVID_SUDI created succesfully
*Nov 19 14:53:38.266: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named CISCO_IDEVID_SUDI has been generated or imported by pki-sudi
*Nov 19 14:53:39.671: %SYS-6-BOOTTIME: Time taken to reboot after reload =  200 seconds
*Nov 19 14:53:39.708: %PKI-6-TRUSTPOINT_CREATE: Trustpoint: CISCO_IDEVID_SUDI0 created succesfully
*Nov 19 14:53:39.720: %PKI-2-NON_AUTHORITATIVE_CLOCK: PKI functions can not be initialized until an authoritative time source, like NTP, can be obtained.
*Nov 19 14:53:39.786: %PKI-6-TRUSTPOINT_CREATE: Trustpoint: TP-self-signed-1007201388 created succesfully
*Nov 19 14:53:40.081: %PKI-4-NOCONFIGAUTOSAVE: Configuration was modified.  Issue "write memory" to save new IOS PKI configuration
*Nov 19 14:53:40.699: %SPA_OIR-6-ONLINECARD: SPA (C1117-LTE) online in subslot 0/2
*Nov 19 14:53:42.147: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named ssh-key.server has been generated or imported by crypto-engine
*Nov 19 14:53:42.842: new extended attributes received from iomd(slot 0 bay 4 board 0)
*Nov 19 14:53:43.597: %SPA_OIR-6-ONLINECARD: SPA (ISR-AP1100AC-E) online in subslot 0/4
*Nov 19 14:53:46.756: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/0, changed state to up
*Nov 19 14:53:46.864: %LINK-3-UPDOWN: Interface Wlan-GigabitEthernet0/1/4, changed state to up
*Nov 19 14:53:47.812: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0/0, changed state to up
*Nov 19 14:53:47.865: %LINEPROTO-5-UPDOWN: Line protocol on Interface Wlan-GigabitEthernet0/1/4, changed state to up
*Nov 19 14:53:47.873: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan1, changed state to up
*Nov 19 14:53:57.480: %DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet0/0/0 assigned DHCP address 10.10.10.50, mask 255.255.255.0, hostname ro01

*Nov 19 14:54:02.920: spa in 0/3, still in booting

*Nov 19 14:54:25.034: %IM-6-IOX_ENABLEMENT: R0/0: ioxman: IOX is ready.
*Nov 19 14:54:32.921: spa in 0/3, still in booting

*Nov 19 14:54:36.649: %SPA_OIR-6-ONLINECARD: SPA (C1117-VADSL-M) online in subslot 0/3
Nov 19 14:54:40.108: %PKI-6-AUTHORITATIVE_CLOCK: The system clock has been set.
Nov 19 14:54:41.121: %PKI-6-TRUSTPOINT_CREATE: Trustpoint: SLA-TrustPoint created succesfully
Nov 19 14:54:41.127: %PKI-6-CONFIGAUTOSAVE: Running configuration saved to NVRAM[OK]
Nov 19 14:54:45.604: %SYS-6-PRIVCFG_ENCRYPT_SUCCESS: Successfully encrypted private config file
Nov 19 14:54:45.675: %CALL_HOME-6-CALL_HOME_ENABLED: Call-home is enabled by Smart Agent for Licensing.
Nov 19 14:54:45.907: %SMART_LIC-6-REPORTING_REQUIRED: A Usage report acknowledgement will be required in 364 days.
Nov 19 14:54:49.481: %CELLWAN-5-SIM_DETECT_COMPLETE: [Cellular0/2/0]: SIM presence detection has completed !!
Nov 19 14:54:55.045: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 14:54:55.487: %CELLWAN-2-SIM_NOT_PRESENT: [Cellular0/2/0]: SIM is not present in Slot 0
Nov 19 14:55:34.069: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 14:55:43.098: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 14:55:54.937: %CELLWAN-2-MODEM_UP: Modem in slot 0/2 is now UP
Nov 19 14:55:55.141: %CELLWAN-2-MODEM_RADIO: Cellular0/2/0 Modem radio has been turned on
Nov 19 15:00:43.093: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 15:05:53.167: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 15:11:02.192: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name
Nov 19 15:54:56.672: %SMART_LIC-3-COMM_FAILED: Communications failure with the Cisco Smart License Utility (CSLU) : Unable to resolve server hostname/domain name

ro01#
ro01#
ro01#
ro01#
ro01#
ro01#
ro01#
```
