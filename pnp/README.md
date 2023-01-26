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

---
### IOS-XE Images
Place the IOS-XE images on an HTTP server where the new devices can download them. If you use this PnP server to provide the `images` place them in the images' subdirectory. For the images I would recommend using a _real_ HTTP server.

---
### Configuration files
Create for each device a configuration file named SERIALNUMBER.cfg. i.e.: [`FCZ094210DS.cfg`](pnp/configs/FGL223590FL.cfg). Place the configuration files also on your HTTP server, so the new devices can download them. In case the PnP server should deliver the configuration files, copy them in the `configs` subdirectory.

**Hint**: you can use different HTTP servers for the images and the configuration files

**Note**: the PnP server runs on HTTP. So there is no encryption for the configuration files as the are downloaded by the new devices.

---
### Install the PnP server:

on Linux
```
# clone the git repository
~/: git clone https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision.git

# go to the pnp subproject
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

Running PnP server. Stop with ctrl+c
Bind to IP-address      : ::
Listen on port          : 8080
Image file(s) base URL  : http://192.168.10.133:8080/images
Config file(s) base URL : http://192.168.10.133:8080/configs

```

on Windows
```
c:\>git clone https://thl-cmk.hopto.org/gitlab/bits-and-bytes/cisco_day0_provision.git
c:\>cd cisco_day0_provision\pnp
c:\cisco_day0_provision\pnp>python -m venv .venv
c:\cisco_day0_provision\pnp>.venv\Scripts\activate.bat

(.venv)c:\cisco_day0_provision\pnp>pip install flask
(.venv)c:\cisco_day0_provision\pnp>pip install xmltodict
(.venv)c:\cisco_day0_provision\pnp>pip install requests
(.venv)c:\cisco_day0_provision\pnp>pip install python-dotenv

(.venv)c:\cisco_day0_provision\pnp>python open-pnp.py

Running PnP server. Stop with ctrl+c
Bind to IP-address      : ::
Listen on port          : 8080
Image file(s) base URL  : http://192.168.10.133:8080/images
Config file(s) base URL : http://192.168.10.133:8080/configs

```

You can check if the PnP server is running by opening a web browser and accessing the status page of the pnp server

`http://<your-ip>:8080/status`

![PnP server new status page](pnp-empty-status.png)

---
### Configure the PnP server

to use the PnP server you need to configure the server by modifying the following files

- [**_settings.py_**](/pnp/open-pnp.ini)
- [**_images.py_**](/pnp/images.json)

**NOTE**: after changing the PnP server configuration you need to restart the PnP server.

---
#### Global variables in [**open-pnp.ini_**](/pnp/open-pnp.ini)

```
[settings]
# BIND_PNP_SERVER = '0.0.0.0'
# PORT = 8080
# TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
# STATUS_REFRESH = 60
# DEBUG = False
# LOG_TO_FILE = True
# LOG_FILE = 'log/pnp_debug.log'
IMAGE_BASE_URL = 'http://192.168.10.133:8080/images'
CONFIG_BASE_URL = 'http://192.168.10.133:8080/configs'
# IMAGE_DATA = 'images.json'
```

- **BIND_PNP_SERVER**: the IP-address of your open-pnp server box. (Use `'::'` for IPv6)
- **PORT**: the TCP port the server should listen on (remember for port 80 the server needs to run as root)
- **TIME_FORMAT**: the time format used in the status page
- **STATUS_REFRESH**: the interval in seconds the status page will automatically reload
- **DEBUG**: enable debug output with `DEBUG = True`. Can be `True` or `False`.
- **LOG_FILE**: path/name of the log file
- **LOG_TO_FILE**: write log output to file. Can be `True` or `False`.
- **IMAGE_BASE_URL**: the base URL for your images 
- **CONFIG_BASE_URL**: the base URL for your configuration files
- **IMAGE_DATA**: the file containing the data of your IOS/IOS-XE images

**Note**: you need to uncomment (remove `# `) the lines if you change the values.

---
#### _IMAGES_ dictionary in [**_images.json_**](/images.json)

Each entry in the _IMAGES_ dictionary contains
- the **name** of the image file as key
- the IOS/IOS-XE **version** of the image
- the **md5** checksum of the image file
- the **size** of the image file in bytes
- a list of **models** where that image should be used

```
    "c1000-universalk9-mz.152-7.E7.bin": {
        "version": "15.2(7)E7",
        "md5": "1e6f508499c36434f7035b83a4018390",
        "size": 16499712,
        "models": ["C1000-8T-2G-L", "C1000-24P-4G-L", "C1000-24T-4G-L", "C1000-24T-4X-L", "C1000-48P-4G-L", "C1000-48T-4X-L"]
    }
```

**NOTE:** By default _open-pnp_ expects the image data in _images.json_. You can change this with the key _IMAGE_DATA_ in _settings.ini_.

**NOTE:** this file needs to be in valid json format.

---
### PnP server discovery
The IOS-XE device can discover a PnP server via DHCP option 43 or using DNS lookup for the hostname _pnpserver.your.domain_. Replaced _your.domain_ by the DNS domain the device receives via DHCP. With DHCP, the DHCP server needs to send the vendor option 43.

Structure of DHCP option 43:

- 5: DHCP sub-option for PnP
- A: feature-code for Active
- 1: Version
- D: Debug On
- K: Defines the Transport Protocol as 4 = HTTP
- B: Defines the Server Address as 2 = IPv4
- I: is your Server IP
- J: is your Server Port

Here a sample how to do this on an IOS/IOS-XE switch.
```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 43 ascii 5A1D;K4;B2;I192.168.10.15;J8080
 lease 0 2
```
For more details on PnP server discovery options see [PnP server discovery](https://developer.cisco.com/site/open-plug-n-play/learn/learn-open-pnp-protocol/). There you will also find an overview how the PnP protocol works. 

---
### PnP Status page

You can monitor the PnP progress on the PnP server status page.

![PnP server status page](sample-pnp-status.png)

**Hint** you can change the status page output by modifying the [**_status.html_**](/pnp/templates/status.html) file in the templates' subdirectory.
