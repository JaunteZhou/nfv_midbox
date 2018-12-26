# [OpenStack Neutron配置虚拟机访问外网](https://www.cnblogs.com/edisonxiang/p/7365627.html)



https://www.cnblogs.com/edisonxiang/p/7365627.html



**配置完成后的网络拓扑如下：**

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815160538256-1012288236.png)

 

**当前环境：**

X86服务器1台

Ubuntu 16.04

DevStack搭建OpenStack

**网络拓扑：**

外部网络：192.168.98.0/24

内部网络：10.0.0.0/24

网络连接： Flat Bridge

 

**1.    通过Horizon按顺序删除已有的Router、Public和Private网络。**

注：DevStack默认安装的Public网络为172.24.4.1/24，经常都不能与生产或者实验环境的网络匹配，故先删除掉当前已用网络。

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815161449162-1129320532.png)     

 

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815161501021-673694911.png)

 

**2.    编辑/etc/network/interfaces，填写如下内容。**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto p4p1
iface p4p1 inet static
address 0.0.0.0
netmask 0.0.0.0

auto br-ext
iface br-ext inet static
address 192.168.98.122
netmask 255.255.255.0
gateway 192.168.98.1
dns-nameservers 218.6.200.139
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```

```

注：p4p1为X86服务的物理网卡名称，br-ext为待使用的bridge。

 

**3.     删除DevStack默认创建的虚拟bridge。**

注：OpenStack Neutron默认使用Openvswitch进行网络虚拟化。

使用下述命令查看DevStack默认创建的虚拟bridge。

$ ovs-vsctl show

使用下述命令删除DevStack默认创建的虚拟bridge。

$ ovs-vsctl del-br br-ex

$ ovs-vsctl del-br br-int

$ ovs-vsctl del-br br-tun

 

**4.     修改Neutron原有的Physical Network（从Public修改ext）。**

编辑/etc/neutron/plugins/ml2/ml2_conf.ini，修改下述蓝色部分。

[ml2_type_flat]
flat_networks = ext,

 

[ml2_type_vlan]

network_vlan_ranges = ext

 

[ovs]
datapath_type = system
bridge_mappings = ext:br-ext
tunnel_bridge = br-tun

 

**5.     添加新的虚拟bridge。**

使用下述命令创建的新的虚拟bridge。

$ ovs-vsctl add-br br-ext

$ ovs-vsctl add-port br-ext p4p1

注：p4p1为X86服务的物理网卡名称，br-ext为待使用的bridge。

 

**6.     重启Network和Neutron主服务。**

$ service networking restart

$ service devstack@q-svc restart

$ service devstack@q-agt restart

 

**7.     通过Horizon重新创建PublicSite。**

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815164520225-1971261498.png)

 ![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815164603146-987838093.png)

 ![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815164621646-701348646.png)

```

```

**8.     通过Horizon重新创建PrivateSite。**

 ![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815165133850-1919670790.png)

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815165147084-454682372.png)

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815165200646-133286725.png)

 

**9.     通过Horizon重新创建Router。**

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815165548646-1151190345.png)

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815165602662-1016060903.png)

 

**10.     创建虚拟机并分配Floating IP。**

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815170011896-1651655947.png)

 

**11.     设置Security Group保证可以Ping和SSH到Floating IP。**

![img](https://images2017.cnblogs.com/blog/83241/201708/83241-20170815170447975-2083320174.png)

注：Security Group Rules如下：

ALL ICMP INGRESS CIDR 0.0.0.0

ALL TCP INGRESS CIDR 0.0.0.0

 

**12.     完成后测试创建的虚拟机能否访问外网以及外网能否通过Floating IP访问创建的虚拟机。**