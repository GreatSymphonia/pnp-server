# Zero Touch Provisioning (ZTP) for IOS XE based devices 

# Introduction

When a device that supports python Zero-Touch Provisioning boots up, and does not find the startup configuration 
(during fresh installation on Day Zero), the device enters the Zero-Touch Provisioning mode. The device locates a 
Dynamic Host Control Protocol (DHCP) server, bootstraps itself with its interface IP address, gateway, and Domain Name 
System (DNS) server IP address, and enables Guest Shell. The device then obtains the IP address or URL of a TFTP/HTTP 
server, and downloads the Python script to configure the device. Guest Shell provides the environment for the Python 
script to run. Guest Shell executes the downloaded Python script and configures the device for Day Zero. After Day Zero 
provisioning is complete, Guest Shell remains enabled.

### Acknowledgment 
This project is based on  https://github.com/cisco-ie/IOSXE_ZTP

- Jeremy Cohoe (jcohoe) jcohoe@cisco.com . His XE ZTP script is a starting point for the codebase
- Arun Kumar Sakthivel (arsakthi@cisco.com) and  Chitransh Pratyush (cpratyus) cpratyus@cisco.com created the 
  repository on github

## Prerequisites

- Your devices needs to be ZTP capable. This is true for most IOS-XE devices like ISR routers, Catalyst 9k Switches, 
ASR routers and so on.
- a file server to store the images, config files and the ztp script (recommended is an HTTP server)  
- a DHCP server to provide IP configuration and option 67 to the new devices 

**Note:** there needs to be one config file for each device with the name SERIALNUMBER.cfg. SERIALNUMBER needs to be 
replaced by the exact serial number of the device.

**Note:** HTTP-based download of ZTP Python script available as of 16.8.1.

**Note:** ZTP not supported in IOS XE 16.12.4 due to a defect.

## How to use

Modify the [**_ztp.py_**](ztp.py) script for your needs.

- you need to modify the _software_images_ dictionary to contain all the images you want to use.
- you need to modify the _models_ dictionary to have one entry for all device models you have pointing to the correct 
  entry in the _software_images_ dictionary
- set the global variables

Second place this script, the image(s) and configuration files on a file server where the new device(s) can download 
them from. This can be a TFTP, HTTP(S), FTP or SCP server. For the image I would not recommend using TFTP. You can [follow the process on the console](sample_output.md), but dont touch anything.

**Note:** To speed up the image transfer, put the image on an USB stick and connect them to the new device. The script will first look on `usb0:` to find the image file before downloding it from the file server.

### _software_images_ dictionary

Each entry in the _software_images_ dictionary contains
- a unique name, i.e., the product family + version
- the name of the image file
- the IOS-XE version of the image
- the md5 sum of the image file
- (optional) if install mode is required or not


```
'C1100_17_06_03': SoftwareImage(
    image='c1100-universalk9.17.06.04.SPA.bin',
    version='17.06.04',
    md5_image='2caa962f5ed0ecc52f99b90c733c54de',
    install_mode=True
)
```

### _models_ dictionary

Each entry in the _models_ dictionary contains
- a unique name that exactly matches the model name of the device
- a pointer to the image for this model in the _software_images_ dictionary
- (optional) if install mode is required or not


```
'C1117-4PMLTEEAWE': Model(
    image='C1100_17_06_04',
    model='C1117-4PMLTEEAWE',
    install_mode=False,
)
```

### global variables

- _http_image_: the ip address of the HTTP server where your images are stored
- _http_config_: the ip address of the HTTP server where your config files are stored
- _ntp_server_:  the ip address of your NTP server to synchronize time stamps of log messages (disable with 'ntp_server=None')
- _syslog_server_: the ip address of yor syslog server (disable with 'syslog_server=None')
- _console_log_level_: the log level on the console, default is `emergencies` for a clean output
- _log_to_file_: set to `False` to disable the creation of a logfile (default is `True`). The logfile is under `flash:/guest-share/ztp.log`.
- _switch_to_install_mode_: set to `False` to use bundle mode by default, can be overridden in _models_/_software_images_ on the model or image level
- _verbose_: if set to `True` the script will show each single exec/config command on the console by using 
  `executep`/`configurep` insted of `execute`/`configure` 

Sample global variables section
```    
http_image = '192.168.10.15'
http_config = '192.168.10.15'
ntp_server = '10.10.10.1'
syslog_server = '10.10.10.1'
console_log_level = 'emergencies'
log_to_file = True
switch_to_install_mode = True
verbose = False
```    

## Deployment
When an XE device boots and there is no config and when DHCP provides option 67 with this python file from repo, 
it will be automatically downloaded to device and gets executed.

### DHCP Server
A DHCP server is required for ZTP, as this is how the device learns about where to find the Python configuration file 
from. In our case, the DHCP server is the open source ISC DHCPd and the configuration file is at /etc/dhcp/dhcpd.conf 
in a Linux developer box. The option bootfile-name is also known as option 67 and it specifies the python file ztp.py

Below is a sample dhcpd.conf and someuseful commands for ISC DHCP server for your use. 
```    
    option domain-name "lab_name";
    default-lease-time 600;
    max-lease-time 7200;
    ddns-update-style none;
    authoritative;
    subnet x.x.x.x netmask x.x.x.x {
    range 10.1.1.150 10.1.1.159;
    option domain-name "";
    option domain-name-servers x.x.x.x;
    option subnet-mask x.x.x.x;
    option broadcast-address 1x.x.x.x;
    option routers x.x.x.x;
    option ntp-servers x.x.x.x;
    default-lease-time 600000;
    max-lease-time 720000;

    class "C9300-24T" { match if substring (option vendor-class-identifier,0,15) = "\tC9300-24T"; }
    
      pool {
        allow members of "C9300-24T";
        deny members of "ciscopnp";
        range x.x.x.x x.x.x.x;
        option bootfile-name "http://x.x.x.x/ztp.py";
      }
```

Here a sample how to do this on an IOS/IOS-XE switch.
```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 67 ascii http://192.168.10.15/ztp.py
 lease 0 2
```

#### Useful DHCP commands 
cat /etc/dhcp/dhcpd.conf | grep bootfile-name

Example for DHCP Option 67 bootfile-name with HTTP:
option bootfile-name "http://x.x.x.x/ztp.py";

ps xa |grep dhcpd

tail -F /var/log/dhcpd.log &

In our case the Python file for ZTP is called ztp.py and is hosted at the webserver root directory which is set 
within the Apache webserver configuration.

### Web Server
ZTP accesses the python configuration file from HTTP or TFTP server(In our case we use HTTP).
Before running ZTP check that the Apache HTTPD server is running with the following commands, this will follow the log 
file from the webserver so you will see when the file is accessed.

ps xa | grep httpd

tail -F /var/log/httpd/access_log & 

### What this python script (from this repo) do? 

- Gets downloaded automatically to the device.
- Start execution in the guest shell.
- Logs ZTP process to persistent storage on the device flash for failure analysis.
- checks if upgrade/downgrade required and takes appropriate action.
- If upgrade required, transfers image from http server to device flash. 
- upgrades the device
- removes any old images 
- (optional) switches from bundle mode to install mode
- Pushes the entire golden config or a partial config.
- Notifies user of success/failure on both CLI prompt and logs.

## Support Information

- GuestShell/ZTP needs 1.1GB free space on bootflash.  May be unable to launch GuestShell to execute ZTP if < 1.1 GB 
  is free on bootflash.
- Md5 checksum will fail on IOSXE V16.6 and V16.7 due to known issue , so the script will bypass that MD5 checksum on 
  that specific versions and continue with the rest of the workflow
- On 16.6.x and 16.7.x  ZTP If image file transfer need to happen , it *might* intermittently fail for first time and 
  ZTP could report fail ,but an *automatic* re attempt will be done and it should be successful in the subsequent 
  attempt.

### Health Monitoring

Log Files from running this Python Script are enabled by default , Logging can be disabled by setting the flag 
log_tofile = False in the script. On IOS XE 17.2.x and above log files are stored at '/flash/guest-share/ztp.log'. 
In all other version logs will be located at '/flash/ztp.log'

