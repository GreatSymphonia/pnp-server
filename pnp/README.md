# Plug and Play (PnP) server for IOS XE based devices 

# Introduction

This is a basic implementation of the Cisco Plug and Play protocol, to fully automate the day0 provisioning of Cisco IOS-XE devices.

### Acknowledgment 
This project is based on https://github.com/oliverl-21/Open-PnP-Server


## Prerequisites

- Your devices need to be PnP capable. This is true for most IOS-XE devices like ISR routers, Catalyst 9k Switches, 
ASR routers and so on.
- a HTTP server to store the images and config files
- a DHCP server to provide IP configuration and option 43 to the new devices (or DNS)
- an python 3.x environment to run this PnP server

## How to use

### IOS-XE Images
Place the IOS-XE images on a HTTP server where the new device can download them.

### Configuration files
Create for ach device a configuration file named SERIALNUMBER.cfg. i.e.: `FCZ094210DS.cfg`. Place the configuration files also on an HTTP server so the new devices can download them. 

**Hint**: you can use different HTTP servers for the images and the configuration files

**Note**: the PnP server runs on HTTP. So there is no encryption for the configuration files as the are dwonloaded by the new devices.

### Install the PnP server:

```
# clone the git repository
~/: git clone https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision.git

# got to the pnp subproject
~/: cd cisco_day0_provision/pnp

# create a python virtual environment (optional)
~/cisco_day0_provision/pnp$ python3.8 -m venv .venv

# activate the environment
~/cisco_day0_provision/pnp$ source .venv/bin/activate

# update pip (oprional)
(.venv) :~/cisco_day0_provision/pnp$ pip3 install -U pip

# install the required pyton packages
(.venv) :~/cisco_day0_provision/pnp$pip3 install -r requirements.txt

# run the pnp server
(.venv) :~/cisco_day0_provision/pnp$ python3.8 open-pnp.py 
runnig PnP server. Stop with ctrl+c

```

You can check if the PnP server is running by opening a webbrowser and accessing the status page of the pnp server

`http://<your-ip>:8080/status`


### Configure the PnP server

to use the PnP server you need to configure the server by modifying the 

- vars.py
- images.py
- platforms.py 

files in the `vars` subbdirectory.

**Note**: after changing the PnP server configuration you need to restart teh PnP server.

#### Global variables in vars.py

```
BIND_PNP_SERVER = '0.0.0.0'
PORT = 8080
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%Z'
STATUS_REFRESH = 60
IMAGE_BASE_URL = 'http://192.168.10.15'
CONFIG_BASE_URL = 'http://192.168.10.15'
FLASK_DEBUG = False
```

- **BIND_PNP_SERVER**: the IP-adress of your python box
- **PORT**: the TCP port the server should listen (rember for port 80 the server needs to run as root)
- **TIME_FORMAT**: the time format used in the status page
- **STATUS_REFRESH**: the intervall the status page will automatically reload
- **IMAGE_BASE_URL**: the base URL for your images
- **CONFIG_BASE_URL**: the base URL for your configuration files
- **FLASK_DEBUG**: enable flask debug output with `FLASK_DEBUG=True`

#### _IMAGES_ dictionary in images.py

Each entry in the _software_images_ dictionary contains
- a unique name, i.e., the product family + version
- the name of the image file
- the IOS-XE version of the image
- the md5 sum of the image file
- (optional) if install mode is required or not

```
'C1100_17_06_04': SoftwareImage(
    image='c1100-universalk9.17.06.04.SPA.bin',
    version='17.06.04',
    md5_image='2caa962f5ed0ecc52f99b90c733c54de',
    install_mode=True
    size=651402492,
)
```

#### _PLATFORMS_ dictionary in platforms.py

Each entry in the _PLATFORMS_ dictionary contains
- a unique name that exactly matches the model name (PID) of the device
- a pointer to the image for this model in the _IMAGES_ dictionary

```
'C1117-4PMLTEEAWE': Model(
    image='C1100_17_06_04',
)
```

### PnP server discovery
An IOS-XE device can discover a PnP server via DHCP option 43 or using DNS lookup for the hostname _pnpserver.your.domain_. Where _your.domain_ will be replaced by the DNS domain the dievice recives via DHCP. In case of DHCP, the DHCP server needs to send the vendor option 43.

- 5: DHCP sub-option for PnP
- A: feature-code for Active
- 1: Version
- D: Debug On
- K: Defines the Transport Protocol as 4 = HTTP
- B: Defines the Server Adress as 2 = IPv4
- I: is your Server IP
- J: is your Server Port

Here a sample how to do this on an IOS/IOS-XE switch.
```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 43 ascii 5A;K4;B2;I192.168.10.15;J8080
 lease 0 2
```
For more details on PnP server dicovery options see [PnP server discovery](https://developer.cisco.com/site/open-plug-n-play/learn/learn-open-pnp-protocol/). There you will also find an overview how the PnP protocol works. 

### Health Monitoring

You can monitor the PnP progress on the PnP server status page.
