This is a basic script used to automatically update Cisco IOS/IOS-XE devices on day0. For this to work it uses DHCP option 67 that points to this script.

## How to use

First plase the image to install in the new device also on a fileserver the device can reach. This can be a TFTP, HTTP(S), FTP or SCP server. For the image I would not recommend using TFTP.

Second modify the script to your liking. You need this information. USERNAME and PASSWORD ar optional if your file server dont use authentication. 

- HTTPSERVERIP = 192.168.10.15
- IMAGENAME = c1100-universalk9.17.06.03a.SPA.bin
- DSTINATIONFLASH = flash
- USERNAME = update
- PASSWORD = update

Third place the script on a fileserver the new device can reach. 

Last configure your DHCP server to have option 67 pointing to this script.

```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 domain-name home.intern
 option 67 ascii http://192.168.10.15/autoinstall.txt
 lease 0 2
```

Now you are ready to attach your new device to the network and switch it on. Wait till the autoinstall process is done. You can follow the process on the console, but touch anything.

If everything works, your device will download the new image, set the boot variable, reboots and erases its startup-configuration. 
