This is a basic script used to automatically update Cisco IOS/IOS-XE devices on day0. For this to work it uses DHCP option 67 that points to this script.

## How to use

First place this script and the image you want to install on a fileserver where the new device can reach it. This can be a TFTP, HTTP(S), FTP or SCP server. For the image I would not recommend using TFTP.

Second modify the script to your liking (replace all the <> placeholders with your values, including <>). 

You need this information. 

- SERVERIP = 192.168.10.15
- PROTOCOLL = HTTP
- IMAGENAME = c1100-universalk9.17.06.03a.SPA.bin
- DSTINATIONFLASH = flash
- USERNAME = update
- PASSWORD = update

USERNAME and PASSWORD are optional. If your file server doesn't uses authentication remove `<USERNAME>:<PASSWORD>@` from the copy command. 

Last configure your DHCP server to have option 67 pointing to this script. Here a sample how to do this on a IOS/IOS-XE switch.

```
ip dhcp pool autoinstall
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 option 67 ascii http://192.168.10.15/autoinstall.txt
 lease 0 2
```

Now you are ready to attach your new devices to the network and switch it on. Wait till the autoinstall process is done. You can follow the process on the console, but touch anything.

If everything works, your device gets an IP-address and the path to the script via DHCP, downloads the script, downloads the new image, sets the boot variable, reboots and erases its startup-configuration and any old images. 
