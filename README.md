# Cisco day0 provisioning

### Introduction
When a network device like a switch or a router comes the first time on-line, a fair amount of manual configuration has 
to happen before it is fully functional. At minimum, it needs to be updated to the proper software image and a golden 
configuration. Day zero automation techniques automate these processes, bringing up network devices into a functional 
state with minimal to no-touch. Hence the name Zero touch. The goal of Zero touch is to enable you to plug in a new 
network device and have it configured and transitioned into production automatically without the need for manual 
configuration. For this purpose Cisco offers (at least) three different ways.

- [Autoinstall](/autoinstall/README.md)
- [Zero Touch Provisioning (ZTP)](/ztp/README.md)
- [Plug and Play (PnP)](/pnp/README.md)

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

With [**_autoinstall_**](/autoinstall/README.md) you can update lot of different devices at the same time in a fully automated way. The devices can be IOS or IOS-XE devices cababil of running EEM scripts.

---
### ZTP

With [**_ZTP_**](/ztp/README.md) you can update and configure a lot of different devices at the same time in a fully automated way. ZTP uses the day0 pyton guest shell on IOS-XE devices.

---
### PnP

not yet implemented.
