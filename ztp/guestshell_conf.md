```
!
! Sampleconfig for guestshell with ssh access
!
!
! Cisco Apphosting Doc
! https://developer.cisco.com/docs/iox/#!tutorial-create-custom-package-descriptor-for-docker-apps/tutorial-create-custom-package-descriptor-for-iox-docker-app
! https://github.com/cisco-ie/IOSXE_ZTP
! https://0x2142.com/getting-started-with-ios-xe-guestshell/
!
!
username admin privilege 15 secret 0 <replaced>
!
interface Vlan1
 ip address 192.168.10.124 255.255.255.0
 ip nat outside
!
interface VirtualPortGroup0
 ip address 192.168.35.1 255.255.255.0
 ip nat inside
!
ip http server
ip http authentication local
ip http secure-server
!
ip access-list standard acl-nat-iox
 20 permit 192.168.35.0 0.0.0.255
!
! enable access form guestshell to outside
ip nat inside source list acl-nat-iox interface Vlan1 overload
!
! access guestshell via ssh from outside
ip nat inside source static tcp 192.168.35.2 22 192.168.10.124 2222 extendable
!
iox
!
app-hosting appid guestshell
 app-vnic gateway0 virtualportgroup 0 guest-interface 0
  guest-ipaddress 192.168.35.2 netmask 255.255.255.0
 app-default-gateway 192.168.35.1 guest-interface 0
 name-server0 192.168.10.12
 start
!
line con 0
 privilege level 15
 logging synchronous
 width 150
 transport input none
 stopbits 1
line vty 0 31
 exec-timeout 120 0
 privilege level 15
 logging synchronous
 login local
 width 15
 transport input ssh
!
end

```
