# Zero Touch Provisioning (ZTP) for IOS XE based devices 

# Introduction

When a device that supports python Zero-Touch Provisioning boots up, and does not find the startup configuration (during fresh install on Day Zero), the device enters the Zero-Touch Provisioning mode. The device locates a Dynamic Host Control Protocol (DHCP) server, bootstraps itself with its interface IP address, gateway, and Domain Name System (DNS) server IP address, and enables Guest Shell. The device then obtains the IP address or URL of a TFTP/HTTP server, and downloads the Python script to configure the device. Guest Shell provides the environment for the Python script to run. Guest Shell executes the downloaded Python script and configures the device for Day Zero. After Day Zero provisioning is complete, Guest Shell remains enabled.

This project is cloned from  https://github.com/cisco-ie/IOSXE_ZTP

## How to use

First place this script and the image you want to install on a fileserver where the new device can reach it. This can be a TFTP, HTTP(S), FTP or SCP server. For the image I would not recommend using TFTP.

Modify the **_ztp.py_** script for you needs.

- you need to modify the _software_images_ dictionary to contain all the images you want to use.
- you need to mofify the _models_ dictionary to have one entry for all device models you have pointing to the correct entry in the _software_images_ dictionary



### _software_images_ dictionary

Each entry in the _software_images_ dictionary contains
- an unique name, i.e. the product family
- the name of the image to use
- the version of the image
- the md5 summ of the image
- (optional) if install mode is required or not


```
'C1100': SoftwareImage(
    image='c1100-universalk9.17.06.04.SPA.bin',
    version='17.06.04',
    md5_image='2caa962f5ed0ecc52f99b90c733c54de',
    install_mode=True
)
```

### _models_ dictionary

each entry in the _models_ dictionary contains
- a unique name that exacly matches the model number of the divice
- a pointer to the image for this model in the _software_images_ dictionary
- (optional) if install mode is required or not


```
'C1117-4PMLTEEAWE': Model(
    image='C1100_17_06_04',
    model='C1117-4PMLTEEAWE',
    install_mode=False,
)
```





## Prerequisites

|Platform	           |       ZTP Minimum Release	   |       XE Minimum Release
|------------------  |  :-------------------------: |-------------------------:
|Catalyst 9200	      |  16.12.1	                    |    16.9.2
|Catalyst 9300/9500	 |  16.5.1a	                    |    16.5.1a
|Catalyst 9800	      |  16.12.1	                    |    16.10.1
|ASR 1000 Fixed	     |  16.7.1	                     |   3.12.0 (1001-X) / 16.2.1 (1002-HX)
|ASR 1000 Modular	   |  16.8.2	                     |   Varies (3.x)
|Catalyst 8000	      |  17.3.2	                     |   17.3.2

HTTP-based download of ZTP Python script available as of 16.8.1.

ZTP not supported in IOS XE 16.12.4 due to a defect.

ZTP solution requires a DHCP server, which will inform the network device about where to find python file/configuration/software image etc to download. This can be a location on the network and can be on a TFTP or HTTP server.


## Deployment
When an XE device boots and there is no config and when DHCP provides option 67 with this python file from repo, it will be automatically downloaded to device and gets executed.

### DHCP Server
A DHCP server is required for ZTP, as this is how the device learns about where to find the Python configuration file from. In our case, the DHCP server is the open source ISC DHCPd and the configuration file is at /etc/dhcp/dhcpd.conf in a Linux developer box. The option bootfile-name is also known as option 67 and it specifies the python file ztp.py

Below is a sample dhcpd.conf and someuseful commands for ISC DHCP server for your use. 
    
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

#### Useful DHCP commands 
cat /etc/dhcp/dhcpd.conf | grep bootfile-name

Example for DHCP Option 67 bootfile-name with HTTP:
option bootfile-name "http://x.x.x.x/ztp.py";

ps xa |grep dhcpd

tail -F /var/log/dhcpd.log &

In our case the Python file for ZTP is called ztp.py and is hosted at the webserver root directory which is set within the Apache webserver configuration.

### Web Server
ZTP accesses the python configuration file from HTTP or TFTP server(In our case we use HTTP).
Before running ZTP check that the Apache HTTPD server is running with the following commands, this will follow the log file from the webserver so you will see when the file is accessed.

ps xa | grep httpd

tail -F /var/log/httpd/access_log & 

### What this python script (from this repo) do? 

Gets downloaded automatically to the device.

Start execution in the guest shell.

Logs ZTP process to persistent storage on the device flash for failure analysis.

Expects input from user about http server address, target version to upgrade/downgrade, image name, image MD5.

checks if upgrade/downgrade required and takes appropriate action.

If upgrade required, transfers image from http server to device flash.

Deploys an EEM script to perform upgrade steps and post upgrade(cleanup) steps.

Runs the EEM script. 

Pushes the entire golden config or a partial config.

Notifies user of success/failure on both CLI prompt and logs.

## Usage

See the support matrix above and use this script accordingly. This script is tested across all XE versions that supports ZTP.


## Support Information

•	GuestShell/ZTP needs 1.1GB free space on bootflash.  May be unable to launch GuestShell to execute ZTP if < 1.1 GB is free on bootflash.

•	Md5 checksum will fail on IOSXE V16.6 and V16.7 due to known issue , so the script will bypass that MD5 checksum on that specific versions and continue with the rest of the workflow

•	On 16.6.x and 16.7.x  ZTP If image file transfer need to happen , it *might* intermittently fail for first time and ZTP could report fail ,but an *automatic* re attempt will be done and it should be successful in the subsequent attempt.


### Support Contacts

Arun Kumar Sakthivel (arsakthi) <arsakthi@cisco.com>

Chitransh Pratyush (cpratyus) <cpratyus@cisco.com>

### Health Monitoring

Log Files from running this Python Script are enabled by default , Logging can be disabled by setting the flag log_tofile = False in the script
On IOS XE 17.2.x and above log files are stored at '/flash/guest-share/ztp.log'. In all other version logs will be located at '/flash/ztp.log'

## Authors

Arun Kumar Sakthivel (arsakthi@cisco.com)

Chitransh Pratyush (cpratyus) <cpratyus@cisco.com>

## License

This project is covered under the terms described in [LICENSE](./LICENSE)


## Acknowledgment 

Jeremy Cohoe (jcohoe) <jcohoe@cisco.com> . His XE ZTP script is a starting point for our codebase. 
