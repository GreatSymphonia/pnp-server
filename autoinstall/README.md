This is a basic script used to automatically update and configure Cisco IOS/IOS-XE devices on day0. For this to work it uses DHCP option 67 that points to this script.

## How to use

First modify the script [**_autoinstall.txt_**](autoinstall.txt) with your values. 

You need this information. 
  - image source i.e.: http://192.168.10.15
  - config source i.e.: http://192.168.10.15
  - ntp server (optional) i.e.: 10.10.10.1
  - log server (optional) i.e.: 192.168.10.15
  - model PID(s) i.e.: C1117-4PMLTEEAWE or WS-C3560CG-12TC-S
  - serial number of each device i.e.: FCZ094210DS

In section 0000 set your global values

```
 action 0000.00 set _image_source "http://192.168.10.15"
 action 0000.01 set _config_source "http://192.168.10.15"
 action 0000.02 set _ntp_server "10.10.10.1"
 action 0000.03 set _log_server "192.168.10.15"
```

If you dont use a ntp or log server set this values like this

```
 action 0000.03 set _ntp_server ""
 action 0000.04 set _log_server ""
```

Create for each device family a section in the 0020 to 0029 range.
Each section contains 
 - a list of models from this family separated by `|`
 - the name of the image file for this device family
 - the IOS(XE) version the device should be running

```
 !
 action 0020.05 string first "|$_model|" "|WS-C3560CG-12TC-S|WS-C3560CG-8TC-S|"
 action 0020.10 if $_string_result gt 1
 action 0020.15   set _target_image "c3560c405ex-universalk9-mz.152-2.E10.bin"
 action 0020.20   set _target_version "15.2(2)E10"
 action 0020.25 end
 !
```

Create for each device a config file named serialnumber.cfg, i.e: [`FCZ094210DS.cfg`](sample.cfg)

Place this script, the image(s) and the config files on a fileserver where the new devices can download them from. This can be a TFTP, HTTP(S), FTP or SCP server. For the image I would not recommend using TFTP.

Last configure your DHCP server to have option 67 pointing to this script. Here a sample how to do this on a IOS/IOS-XE switch.

```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 67 ascii http://192.168.10.15/autoinstall.txt
 lease 0 2
!
```

You can use an IOS/IOS-XE switch to deliver the autoinstall script like this. `192.168.10.1` is the IP-address of the switch

```
tftp-server flash:/autoinstall.txt
!
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 150 ip 192.168.10.1
 option 67 ascii autoinstall.txt
 lease 0 2
!
```

If the imgae you want to deliver fits on the swicth you can also use the switch to deliver the image via http.
**Note**: if you do so, you add the user authentication to your imgae/configuration source i.e. `http://update:update@192.168.10.1`

```
username update privilege 15 password 0 update
!
ip http server
ip http authentication local
ip http path flash:
!
```

Now you are ready to attach your new devices to the network and switch it on. Wait till the autoinstall process is done. You can [follow the process on the syslog server or on the console](/autoinstall/sample_output.md), but dont touch anything.

If everything works, your device gets an IP-address and the path to the script via DHCP, downloads the script, downloads the new image, sets the boot variable, downloads the config file, reboots and finishes the configuration. 
