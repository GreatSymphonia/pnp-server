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

This is a collection of some basic scripts to get these things up and running. All thes methods expect the devices in a factory reset state. 

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

With [**_autoinstall_**](/autoinstall/) you can update and configury many different devices at the same time in a fully automated way. The devices can be **IOS or IOS-XE** devices able of running **EEM** scripts.

---
### ZTP (Zero Touch Provisioning)

With [**_ZTP_**](/ztp/) you can update and configure many of different devices at the same time in a fully automated way. ZTP uses the **day0 pyton guest shell** on **IOS-XE** devices.

---
### PnP (Plug and Play)

With [**_PnP_**](/pnp/) you can update and configure many of different devices at the same time in a fully automated way. PnP uses the Cisco Plug and Play protocol. This available on most(?) **IOS-XE** devices.
