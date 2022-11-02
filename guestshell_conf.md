!
interface Vlan1
 ip address dhcp
 ip nat outside
!
interface VirtualPortGroup0
 ip address 192.168.35.1 255.255.255.0
 ip nat inside
 no mop enabled
 no mop sysid
!
ip http server
ip http authentication local
!
ip access-list standard acl-nat-iox
 20 permit 192.168.35.0 0.0.0.255
!
ip nat inside source list acl-nat-iox interface Vlan1 overload
!
iox
!
app-hosting appid guestshell
 app-vnic gateway0 virtualportgroup 0 guest-interface 0
  guest-ipaddress 192.168.35.2 netmask 255.255.255.0
 app-default-gateway 192.168.35.1 guest-interface 0
 start
