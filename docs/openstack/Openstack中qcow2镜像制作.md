# Openstack中qcow2镜像制作

https://blog.csdn.net/z770816239/article/details/51159232

https://blog.csdn.net/JackLiu16/article/details/80358776

https://blog.csdn.net/weixin_40108079/article/details/77891346

https://my.oschina.net/xiaozhublog/blog/700327







## 深入理解OpenStack-手动制作qcow2镜像

[深入理解OpenStack-手动制作qcow2镜像 - Gary Wu - github.io](https://wuyanteng.github.io/2018/01/18/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3OpenStack-%E6%89%8B%E5%8A%A8%E5%88%B6%E4%BD%9Cqcow2%E9%95%9C%E5%83%8F/)

官方虽提供qcow2系统镜像，但对于有需求的企业来说，还是定制镜像比较靠谱，下面就手动定制一个镜像

### 给虚拟机创建一个网络

手动创建镜像需要确保libvirt运行有default网络，这个网络可以给虚拟机提供上网服务。

查看当前是否启用default网络

```shell
# virsh net-list
 Name                 State      Autostart     Persistent
----------------------------------------------------------
 default              active     yes           yes
```

 注：如果没有启用，使用以下命令启用default

```shell
# virsh net-start default
```

### 创建虚拟机

1. 创建一个目录（可选：用于保存iso镜像和qcow2镜像

```shell
$ mkdir -p /img
```

2. 创建一个10G的磁盘文件给虚拟机使用

```shell
# qemu-img create -f qcow2 /img/centos.qcow2 10G
```

3. 安装kvm

```shell
# virt-install --virt-type kvm --name centos7 --ram 1024 --disk /img/centos.qcow2,format=qcow2 --network network=default --graphics vnc,listen=0.0.0.0 --noautoconsole --os-type=linux --location=/img/CentOS-7-x86_64-Minimal-1611.iso
```

### 使用VNC Viewer连接虚拟机完成安装

1. 要想连接虚拟机就需要执行一条命令来查看刚才新建虚拟机的端口信息

```shell
# netstat -lntup | grep qemu
tcp        0      0 0.0.0.0:5900            0.0.0.0:*               LISTEN      90011/qemu-kvm
tcp        0      0 0.0.0.0:5901            0.0.0.0:*               LISTEN      41365/qemu-kvm 
```

2. 运行VNC Viewer连接虚拟机。Remote Host输入：`IP_ADDRESS:PORT` 进行连接。连接成功后，就看到操作系统的引导界面了，这时候可以对虚拟机进行系统安装了。

   注：只有配置了KVM虚拟机，libvirt就会生成一个与操作系统对应的xml文件，其记录了kvm虚拟机的状态。路径如下：/etc/libvirt/qemu/CentOS-6.6-x86_64.xml  

   注：此文件只能通过“virsh edit”命令修改

### 启动KVM虚拟机

1. 列出所有虚拟机

```
# virsh list --all
 Id    Name                           State
----------------------------------------------------
 7     instance-00000003              running
 12    centos7			              shut off
```

2. 启动虚拟机

```
# virsh  start  centos7
# virsh list --all
```

3. 当此虚拟机再次启动后，再使用VNC Viewer连接。Remote Host输入：`IP_ADDRESS:PORT`进行连接。

   此时可以在此系统中编辑已经提前准备并测试好的系统初始化脚本，并让脚本开机后运行，测试无误后将此虚拟机关机。（此步骤是把开机初始化脚本给封装到镜像中）

   在这个虚拟机系统中运行shutdown -h now 即可

### 关于系统优化脚本-脚本参考

```
#!/bin/bash

set_key(){
  if [ ! -d /root/.ssh ]; then
    mkdir -p /root/.ssh
    chmod 700 /root/.ssh
  fi
# Fetch public key using HTTP
  ATTEMPTS=30
  FAILED=0
  while [ ! -f /root/.ssh/authorized_keys ]; do
    curl -f http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key > /tmp/metadata-key 2>/dev/null
    if [ "$?" -eq 0 ]; then
      cat /tmp/metadata-key >> /root/.ssh/authorized_keys
      chmod 0600 /root/.ssh/authorized_keys
      restorecon /root/.ssh/authorized_keys
      rm -f /tmp/metadata-key
      echo "Successfully retrieved public key from instance metadata"
      echo "*****************"
      echo "AUTHORIZED KEYS"
      echo "*****************"
      cat /root/.ssh/authorized_keys
      echo "*****************"
  else
      FAILED=`expr $FAILED + 1`
      if [ $FAILED -ge $ATTEMPTS ];then
       echo "Failed"
       break
      fi
      sleep 5
  fi
done
}

set_hostname(){
  echo "hehe"
  SET_HOSTNAME=$(curl -s http://169.254.169.254/2009-04-04/meta-data/hostname | awk -F '.' '{print $1}')
   VM_HOSTNAME="$SET_HOSTNAME".example.com
   hostnamectl set-hostname $VM_HOSTNAME
}

set_static_ip(){
  echo "hehe"
   /bin/cp /tmp/ifcfg-eth0-example /etc/sysconfig/network-scripts/ifcfg-eth0
   VM_IPADDR=$(curl -s http://169.254.169.254/2009-04-04/meta-data/local-ipv4)
   sed -i "s/9.9.9.9/$VM_IPADDR/g" /etc/sysconfig/network-scripts/ifcfg-eth0
}

main(){
    set_key;
    set_hostname;
    set_static_ip;
    rm -f /tmp/get_metadata.sh
    /bin/cp /tmp/rc.local /etc/rc.d/rc.local
}
main
```

> 将制作好的/data/centos.qcow2镜像文件上传到Glance

```
注：在控制节点进行镜像上传

(1)source变量
source  /scripts/admin-openrc

(2)镜像上传
openstack image create "CentOS7.4_x86_64" --file /data/centos.qcow2  \
--disk-format qcow2  --public

(3)openstack dashboard中创建虚拟机,并验证脚本执行情况
```

附录：virsh命令-使用

```
virsh --help


virt-clone -o centos7_mini -n centos7_mini15 --auto-clone  #克隆mini，新克隆的为mini15
-o           #原始机名字，必须为关闭或暂停状态
-n           #新客户机的名称
--auto-clone #从原始客户机配置中自动生成克隆名称和存储路径
--replace    #不检查命名冲突，覆盖任何使用相同名称的客户机
-f           #可以指定克隆后的主机镜像放在指定目录下

virsh autostart xxx  #让子机随宿主机开机自动启动
virsh autostart --disable xxx  #解除自动启动

virt-install  #建立kvm虚拟机
virsh list  #查看正在运行的KVM虚拟机
virsh list --all  #查看所有KVM虚拟机
virsh start name   #启动KVM虚拟机
virsh shutdown name #正常关闭KVM虚拟机
virsh destroy name  #强制关闭KVM虚拟机(类似于直接断电)
virsh suspend name  #挂起KVM虚拟机
virsh resume name  #恢复挂起的KVM虚拟机
virsh dumpxml name  #查看KVM虚拟机配置文件，可以把输出的内容定义到xml里，用来克隆迁移用。
virsh edit name  #编辑KVM虚拟机的xml配置文件
virsh define /etc/libvirt/qemu/name.xml  #定义注册虚拟机，需要先查看xml文件对应的镜像，img等路径是否存在或修改指定路径
virsh undefine name  #彻底删除KVM虚拟机,不可逆,如果想找回来,需要备份/etc/libvirt/qemu的xml文件
```

注：gentoo使用livecd安装的过程中，关于安装文件如何上传到livecd的问题，解决方案如下：

```
kvm安装安装启动livecd，然后通过桥接联网将文件上传，再执行脚本安装和初始化。最后将qcow2文件上传到glance。最后通过openstack dashboard来使用qcow2镜像安装gentoo
```





## [解决ubuntu卡在clean, xxx/xxx files, xxx/xxx blocks不能进入系统的问题 - 邪恶天才 - CSDN](https://blog.csdn.net/u013406197/article/details/80773820)

上午的时候ubuntu弹出了一个提示信息，大概通知了一下显卡升级失败的问题，由于着急调试程序，所以就没有理会这个问题，然后下午再开机的时候就发现不能进入系统了，系统一直在 /dev/sda: clean, xxx/xxx files, xxx/xxx blocks这个画面上闪，结合上午的崩溃信息，大概就知道了是显卡驱动出现了问题。

首先先Ctrl+Alt+F1……F6，依次尝试一下，然后会进入到命令行模式，在里面输入用户名和密码，就可以进入到该用户下。

之后，使用  sudo apt-get purge nvidia*  命令更新一下驱动，也可以先卸载掉之前的驱动，再进行更新。

安装完成后  reboot  重启一下发现可以进入系统了。

