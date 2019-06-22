# OpenStack使用前准备工作

## 配置Availability Zone

### 参考文档

https://www.jianshu.com/p/613d34ad6d51

https://www.ibm.com/developerworks/cn/cloud/library/1607-openstack-neutron-availability-zone/index.html

### 步骤

此处针对通过PackStack安装OpenStack之后，需要的准备工作。

首先，增加认证脚本可执行权限：

```shell
$ sudo chmod a+x /root/keystonerc_admin
```

接着，执行认证脚本：

```shell
$ sudo -s source /root/keystonerc_admin
```

查看当前aggregate列表：

```shell
# nova aggregate-list
```

创建az域：

```shell
# nova aggregate-create agg1 az1
# nova aggregate-create agg2 az2
```

将指定主机添加到对应az域的aggregate中：

```shell
# nova aggregate-add-host agg1 controller
# nova aggregate-add-host agg2 compute
```

再次查看当前aggregate列表：

```shell
# nova aggregate-list
```

## 创建OpenStack虚拟网络

### 步骤

进入OpenStack的dashboard界面，确保最上方bar中用户选项为admin，项目选项为admin。

选择左侧菜单栏"Admin"->"Network"->"Networks"，然后点击"+Create Network"按钮添加虚拟网络。

创建过程中，配置Network参数：填写网络名"Name"，选择网络所属项目"Project"为admin，选择"Provider Network Type"为vxlan，勾选Enable Admin State，Shared，Create Subnet。

配置Subnet参数：填写子网名"Subnet Name"，"Network Address"，"Gateway IP"，然后完成创建。

本系统需要创建三个虚拟网络，并将各个虚拟网络的ID值填写到管理中间件的配置文件_config.py中。

