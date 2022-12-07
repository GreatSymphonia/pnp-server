# Cisco day0 provisioning

### Introduction
When a network device like a switch or a router comes the first time on-line, a fair amount of manual configuration has 
to happen before it is fully functional. At minimum, it needs to be updated to the proper software image and a golden 
configuration. Day zero automation techniques automate these processes, bringing up network devices into a functional 
state with minimal to no-touch. Hence the name Zero touch. The goal of Zero touch is to enable you to plug in a new 
network device and have it configured and transitioned into production automatically without the need for manual 
configuration. For this purpose Cisco offers (at least) three different ways.

- [Autoinstall](/autoinstall/)
- [Zero Touch Provisioning (ZTP)](/ztp/)
- [Plug and Play (PnP)](/pnp/)

This is a collection of some basic scripts to get these things up and running. With all this methos you can update and configury many different devices at the same time in a fully automated way. The differnce is what device type are suppoted (IOS/IOS-XE) and the way the are working. All thes methods expect the devices in a factory reset state. 


You can reset a device by issuing the command

```
pnpa service reset no-prompt
```
or on older systems

```
write memory
write erase
reload
```

---
### Want to Contribute?
Nice ;-) Have a look at the [contribution guidelines](CONTRIBUTING.md "Contributing")

---
### Autoinstall

[**_Autoinstall_**](/autoinstall/) suppots **IOS and IOS-XE** devices able of running **EEM** scripts. To use _autoinstall_ you need a DHCP server to provide option 67 (and optionally option 150) to the new devices and some kind of file server where the devices can download the image and configuartihn file from. 

This ist the most basic way for day0 provisioning but still works with most devices.

---
### ZTP (Zero Touch Provisioning)

[**_ZTP_**](/ztp/) supports **only IOS-XE** devices able to run the **day0 pyton guest shell**. To use _autoinstall_ you need a DHCP server to provide option 67 (and optionally option 150) to the new devices and some kind of file server where the devices can download the image and configuartihn file from.

With ZTP you have full access to the new device. So you could configure device from the guestshell insted of only downloading a complete config file.

In newer versions of IOS-XE (i.e.: 19.09.01a no the ISR C1100 family) the guestshell has bekome optionally (separate download), so maybe the days of day0 guestshell are limited.

---
### PnP (Plug and Play)

[**_PnP_**](/pnp/) also supports **only IOS-XE** devices. PnP uses the Cisco Plug and Play protocol. To use PnP you need a DHCP server with option 43 for PnP discovery and this PnP server. PnP is the dya0 provisioning method used bei Cisco DNAC and therfore the preferd method.

