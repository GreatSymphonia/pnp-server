# Cisco day0 provisioning

# Introduction
When a network device like a switch or a router comes the first time on-line, a fair amount of manual configuration has 
to happen before it is fully functional. At minimum, it needs to be updated to the proper software image and a golden 
configuration. Day zero automation techniques automate these processes, bringing up network devices into a functional 
state with minimal to no-touch. Hence the name Zero touch. The goal of Zero touch is to enable you to plug in a new 
network device and have it configured and transitioned into production automatically without the need for manual 
configuration. For this purpose Cisco offers (at least) three different ways.

- Autoinstall
- Zero Touch Provisioning (ZTP)
- Plug and Play (PnP)

This is a collection of some basic scripts to get these things up and running. All thes methods expect the devices in a factory reset state. You can reset a device by issuing the command

```
pnpa service reset no-prompt
```
or on older systems

```
write memory
write erase
reload
```

## Autoinstall

The directory [**_autoinstall_**](/autoinstall) contains a script to get the basic function of updating a device to your desired software image. This is intended to use if you have a lot of identical (from one product family) devices running all with the same image and you just want them to get updated without any manual intervention.

## ZTP

The directory [**_ztp_**](/ztp) contains a script to use the day0 pyton guest shell. You can use this to update and configure different device types at the same time in a fully automated way.

## PnP
