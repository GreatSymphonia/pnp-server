# Cisco day0 provisioning

### Introduction
When a network device like a switch, or a router comes the first time on-line, a fair amount of manual configuration has 
to happen before it is fully functional. At minimum, it needs to be updated to the proper software image and a golden 
configuration. Day zero automation techniques automate these processes, bringing up network devices into a functional 
state with minimal to no-touch. Hence the name Zero touch. The goal of Zero touch is to enable you to plug in a new 
network device and have it configured and transitioned into production automatically without the need for manual 
configuration. For this purpose Cisco offers (at least) three different ways.

- [Autoinstall](/autoinstall/)
- [Zero Touch Provisioning (ZTP)](/ztp/)
- [Plug and Play (PnP)](/pnp/)

This is a collection of some basic scripts to get these things up and running. With all these methods you can update and configure many devices at the same time in a fully automated way. The difference is what device types are supported (IOS/IOS-XE) and the way they are working. All these methods expect the devices in a factory reset state. You can reset a device by issuing the command

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
This is taken from [the original repository of thl-cmk](https://thl-cmk.hopto.org/bits-and-bytes/cisco_day0_provision)
This was modified for use in my private lab and has modifications that make pretty huge assumptions about how you'd like to use it.
If it doesn't fit your use case, please fork it and modify it to your needs. It is mainly up at comply with the GPL license of the original repository.mai


---
### Autoinstall

[**_Autoinstall_**](/autoinstall/) supports **IOS and IOS-XE** devices able of running **EEM** scripts. To use _autoinstall_ you need a DHCP server to provide option 67 (and optionally option 150) to the new devices and some kind of file server where the devices can download the image and configuration file from. 

This is the most basic way for day0 provisioning but still works with most devices.

---
### ZTP (Zero Touch Provisioning)

[**_ZTP_**](/ztp/) supports **only IOS-XE** devices able to run the **day0 python guest shell**. To use _autoinstall_ you need a DHCP server to provide option 67 (and optionally option 150) to the new devices and some kind of file server where the devices can download the image and configuration file from.

With ZTP you have full access to the new device. So you could configure the device from the guestshell instead of only downloading a complete config file.

In newer versions of IOS-XE (i.e.: 19.09.01a on the ISR C1100 family) the guestshell has become optionally (separate download), so maybe the days of day0 guestshell are limited.

---
### PnP (Plug and Play)

[**_PnP_**](/pnp/) supports **IOS-XE and newer IOS** devices. PnP uses the Cisco Plug and Play protocol. To use PnP you need a DHCP server to serve option 43 for PnP discovery and this PnP server. PnP is the dya0 provisioning method used bei Cisco DNAC and therefore the preferred method.

