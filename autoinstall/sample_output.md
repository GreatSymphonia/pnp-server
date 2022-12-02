**Note**: most of the nonrelevant output was removed.

```
System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


........

Located c1100-universalk9.17.06.03a.SPA.bin
########################################################

Package header rev 3 structure detected
IsoSize = 648568832
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
2572272K bytes of USB flash at usb0:.

 WARNING: Command has been added to the configuration using a type 0 password. However, recommended to migrate to strong type-6 encryption
No startup-config, starting autoinstall/pnp/ztp...

Autoinstall will terminate if any input is detected on console



         --- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]:
Autoinstall trying DHCPv4 on Vlan1

Autoinstall trying DHCPv6 on Vlan1

Acquired IPv4 address 10.10.10.12 on Interface Vlan1
Received following DHCPv4 options:
        domain-name     : autoinstall.test
        bootfile        : autoinstall.txt
        dns-server-ip   : 10.10.10.1
        tftp-server-ip  : 10.10.10.1

stop Autoip process
OK to enter CLI now...

pnp-discovery can be monitored without entering enable mode

Entering enable mode will stop pnp-discovery

Attempting bootfile tftp://10.10.10.1/autoinstall.txt



Press RETURN to get started!


*Dec  2 17:05:42.602: %SYS-5-USERLOG_NOTICE: Message from tty0(user id: ): Device in day0 workflow, some non user-configured options may be enabled by default
*Dec  2 17:05:42.613: %SYS-5-CONFIG_P: Configured programmatically by process DHCP Autoinstall from console as vty0
*Dec  2 17:05:47.754: %SYS-5-CONFIG_P: Configured programmatically by process DHCP Autoinstall from console as vty0

*Dec  2 17:05:55.432: %SYS-5-CONFIG_P: Configured programmatically by process DHCP Autoinstall from console as vty0
*Dec  2 17:06:55.762: %EEM-6-LOG: autoinstall: EEM START AUTOINSTALL
*Dec  2 17:06:55.762: %EEM-6-LOG: autoinstall: wait 60s for reload to finish
*Dec  2 17:07:56.380: %SYS-5-LOG_CONFIG_CHANGE: Console logging: level informational, xml disabled, filtering disabled
*Dec  2 17:07:56.382: %SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.10.133 port 514 started - CLI initiated
*Dec  2 17:07:56.943: %SYS-6-CLOCKUPDATE: System clock has been updated from 17:07:56 UTC Fri Dec 2 2022 to 18:07:56 CET Fri Dec 2 2022, configured from console by  on vty0 (EEM:autoinstall).
*Dec  2 17:07:57.190: %SYS-6-CLOCKUPDATE: System clock has been updated from 18:07:57 CET Fri Dec 2 2022 to 18:07:57 CET Fri Dec 2 2022, configured from console by  on vty0 (EEM:autoinstall).
*Dec  2 17:07:57.793: %SYS-5-CONFIG_I: Configured from console by  on vty0 (EEM:autoinstall)
*Dec  2 17:08:04.519: %SYS-6-PRIVCFG_ENCRYPT_SUCCESS: Successfully encrypted private config file
*Dec  2 17:08:04.576: %EEM-6-LOG: autoinstall: wait 60s for interfaces to come up
*Dec  2 17:08:06.880: %DHCP-6-ADDRESS_ASSIGN: Interface Vlan1 assigned DHCP address 10.10.10.12, mask 255.255.255.0, hostname

Dec  2 17:09:05.415: %PKI-6-AUTHORITATIVE_CLOCK: The system clock has been set.
Dec  2 17:09:07.034: %EEM-6-LOG: autoinstall: Model          : |C1117-4PMLTEEAWE|
Dec  2 17:09:07.655: %EEM-6-LOG: autoinstall: S/N            : |FGL223590FL|
Dec  2 17:09:08.081: %EEM-6-LOG: autoinstall: Version        : |17.06.03a|
Dec  2 17:09:08.084: %EEM-6-LOG: autoinstall: Target version : |17.06.04|
Dec  2 17:09:08.084: %EEM-6-LOG: autoinstall: Target image   : |c1100-universalk9.17.06.04.SPA.bin|
Dec  2 17:09:08.495: %EEM-6-LOG: autoinstall: downloading http://192.168.10.15/c1100-universalk9.17.06.04.SPA.bin to flash:
Dec  2 17:29:03.371: %EEM-6-LOG: autoinstall: configure new boot variable
Dec  2 17:29:09.476: %SYS-6-PRIVCFG_ENCRYPT_SUCCESS: Successfully encrypted private config file
Dec  2 17:29:09.754: %SYS-5-CONFIG_I: Configured from console by  on vty0 (EEM:autoinstall)
Dec  2 17:29:16.219: %SYS-6-PRIVCFG_ENCRYPT_SUCCESS: Successfully encrypted private config file
Dec  2 17:29:16.299: %EEM-6-LOG: autoinstall: downloading http://192.168.10.15/FGL223590FL.cfg to startup-config
Dec  2 17:29:20.354: %SYS-0-USERLOG_EMERG: Message from tty1(user id: ): gooing to reload in 5 min


***
*** --- SHUTDOWN in 0:05:00 ---
***

Dec  2 17:29:21.012: %SYS-5-SCHEDULED_RELOAD: Reload requested for 18:34:20 CET Fri Dec 2 2022 at 18:29:20 CET Fri Dec 2 2022 by  on vty0 (EEM:autoinstall). Reload Reason: Reload Command.
Dec  2 17:29:21.023: %EEM-6-LOG: autoinstall: EEM FINISH


***
*** --- SHUTDOWN in 0:01:00 ---
***



***
*** --- SHUTDOWN NOW ---
***

Dec  2 17:34:22.978: %SYS-5-RELOAD: Reload requested by  on vty0 (EEM:autoinstall). Reload Reason: Reload Command.Rom image verified correctly


System Bootstrap, Version 17.5(1r), RELEASE SOFTWARE
Copyright (c) 1994-2021  by cisco Systems, Inc.


Current image running: Boot ROM0

Last reset cause: LocalSoft
C1117-4PMLTEEAWE platform with 4194304 Kbytes of main memory


........

Located c1100-universalk9.17.06.04.SPA.bin
############################################################################

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
2572272K bytes of USB flash at usb0:.


SETUP: new interface Cellular0/2/0 placed in "shutdown" state
SETUP: new interface Cellular0/2/1 placed in "shutdown" state
SETUP: new interface ATM0/3/0 placed in "shutdown" state
SETUP: new interface Ethernet0/3/0 placed in "shutdown" state


Press RETURN to get started!

*Dec  2 17:38:39.808: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan1, changed state to down
*Dec  2 17:38:39.812: %LINEPROTO-5-UPDOWN: Line protocol on Interface Lsmpi0, changed state to up
*Dec  2 17:38:39.815: %LINEPROTO-5-UPDOWN: Line protocol on Interface EOBC0, changed state to up
*Dec  2 17:38:39.818: %LINEPROTO-5-UPDOWN: Line protocol on Interface LIIN0, changed state to up
*Dec  2 17:38:47.091: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named TP-self-signed-1007201388 has been generated or imported by crypto config
*Dec  2 17:38:47.104: %SYS-6-PRIVCFG_DECRYPT_SUCCESS: Successfully apply the private config file
*Dec  2 17:38:47.232: %SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.10.133 port 0 CLI Request Triggered
*Dec  2 17:38:47.397: %SSH-5-DISABLED: SSH 1.99 has been disabled
*Dec  2 17:38:47.423: %SYS-6-CLOCKUPDATE: System clock has been updated from 17:38:47 UTC Fri Dec 2 2022 to 18:38:47 CET Fri Dec 2 2022, configured from console by vty0.
*Dec  2 17:38:47.427: %SYS-6-CLOCKUPDATE: System clock has been updated from 18:38:47 CET Fri Dec 2 2022 to 18:38:47 CET Fri Dec 2 2022, configured from console by vty0.
*Dec  2 17:39:02.498: %SPA_OIR-6-ONLINECARD: SPA (C1117-LTE) online in subslot 0/2
*Dec  2 17:39:02.716: %EEM-6-LOG: finish: EEM START finish config
*Dec  2 17:39:02.716: %EEM-6-LOG: finish: generating ssh key
*Dec  2 17:39:05.855: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named SSH-KEY has been generated or imported by crypto-engine
*Dec  2 17:39:05.997: %SSH-5-ENABLED: SSH 2.0 has been enabled
*Dec  2 17:39:06.048: %SYS-5-CONFIG_I: Configured from console by  on vty0 (EEM:finish)
*Dec  2 17:39:06.058: %EEM-6-LOG: finish: remove EEM script finish config
*Dec  2 17:39:06.544: %SYS-5-CONFIG_I: Configured from console by  on vty0 (EEM:finish)
*Dec  2 17:39:07.840: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named SSH-KEY.server has been generated or imported by crypto-engine
*Dec  2 17:39:12.462: %DHCP-6-ADDRESS_ASSIGN: Interface Vlan1 assigned DHCP address 10.10.10.12, mask 255.255.255.0, hostname ro01

*Dec  2 17:39:14.755: %SYS-6-PRIVCFG_ENCRYPT_SUCCESS: Successfully encrypted private config file
*Dec  2 17:39:14.895: %EEM-6-LOG: finish: EEM END autoinstall

```
