# 修改qcow2c云镜像

## 参考文档

https://zhuanlan.zhihu.com/p/30385809

## 步骤

利用kvm，virsh等虚拟机管理工具以qcow2c磁盘为基础创建新虚拟机。在运行的虚拟机中进行适当的修改和配置之后，运行以下步骤，原qcow2c文件中便已经包含了修改内容，在以后的拷贝创建虚拟机时都会携带修改添加的内容。

在修改后的虚拟机中，执行以下命令：

```shell
# rpm -qa kernel | sed 's/^kernel-//'  | xargs -I {} dracut -f /boot/initramfs-{}.img {} 
```

清除历史命令记录：

```shell
# history -c
```

关闭虚拟机机：

```shell
# /sbin/shutdown -h now
```

然后在宿主机上执行以下命令，移除宿主机信息，比如mac地址等：

```shell
# virt-sysprep -d VM_NAME
```

删除虚拟机，镜像制作完成。

```shell
# virsh undefine VM_NAME
```

原qcow2c镜像文件已经修改完成。