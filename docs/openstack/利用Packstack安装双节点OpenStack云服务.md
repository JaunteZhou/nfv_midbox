# 利用Packstack安装双节点OpenStack云服务

https://www.rdoproject.org/install/packstack/

https://www.rdoproject.org/install/adding-a-compute-node/

http://www.voidcn.com/article/p-nhynorii-bkq.html

https://my.oschina.net/guoba/blog/809001

## 第0步：先决条件

在所有OpenStack节点上执行以下步骤。

### 软件

**Red Hat Enterprise Linux（RHEL）7**是推荐的最低版本，或者是基于RHEL的Linux发行版之一的等效版本，如**CentOS**，**Scientific Linux**等。**x86_64**是目前唯一受支持的架构。

- 有关所需存储[库](https://www.rdoproject.org/documentation/repositories/)的详细信息，请参阅[RDO存储](https://www.rdoproject.org/documentation/repositories/)库。

使用完全限定的域名命名主机，而不是使用短格式名称，以避免与Packstack发生DNS问题。

### 硬件

具有至少16GB RAM的计算机，具有硬件虚拟化扩展的处理器以及至少一个网络适配器。

### 网络

将节点1的第1个网络适配器配置为静态IP地址`10.0.30.51/24`，且开机自启动；将节点2的第1个网络适配器配置为静态IP地址`10.0.30.52/24`，且开机自启动。

针对每个节点，检查/etc/hosts并添加以下内容：

```
10.0.30.51 controller
10.0.30.52 compute 
```

为了对服务器和实例进行外部网络访问，那么需要正确配置网络设置。配置网卡的静态IP地址和禁用NetworkManager。

```shell
$ sudo systemctl disable firewalld
$ sudo systemctl stop firewalld
$ sudo systemctl disable NetworkManager
$ sudo systemctl stop NetworkManager
$ sudo systemctl enable network
$ sudo systemctl start network
```

## 第1步：软件存储库

在所有OpenStack节点上执行以下步骤。

在RHEL上，可以下载并安装RDO存储库RPM以设置OpenStack存储库：

```shell
$ sudo yum install -y https://rdoproject.org/repos/rdo-release.rpm
```

而在CentOS上，Extras存储库提供启用OpenStack存储库的RPM。Extras在CentOS 7上默认启用，因此您只需安装RPM即可设置OpenStack存储库。

```shell
$ sudo yum install -y centos-release-openstack-rocky
```

确保已启用存储库：

```shell
$ yum-config-manager --enable openstack-rocky
```

更新您当前的包：

```shell
$ sudo yum update -y
```

## 第2步：安装Packstack安装程序

在所有OpenStack节点上执行以下步骤。

```shell
$ sudo yum install -y openstack-packstack
```

## 步骤3：准备answer-file配置文件

在OpenStack主节点生成answer-file：

```shell
$ packstack --gen-answer-file=hcloud.txt
```

编辑answer-file配置文件：

```
$ vi hcloud.txt
```

针对answer-file配置文件中以下参数进行修改：

```
CONFIG_CONTROLLER_HOST=10.0.30.51

CONFIG_COMPUTE_HOSTS=10.0.30.51,10.0.30.52

CONFIG_NETWORK_HOSTS=10.0.30.51

CONFIG_STORAGE_HOST=10.0.30.51,10.0.30.52

CONFIG_SAHARA_HOST=10.0.30.51
CONFIG_AMQP_HOST=10.0.30.51
CONFIG_MARIADB_HOST=10.0.30.51
CONFIG_REDIS_HOST=10.0.30.51
```

## 运行Packstack以安装OpenStack

在OpenStack主节点执行以下命令。

首先，安装screen：

```shell
# yum install screen -y
```

Packstack不需要手动设置OpenStack，运行以下命令：

```shell
# screen packstack--answer-file=hcloud.txt
```

有多少节点，就需要依次输入对应节点的密码，部署成功后，出现以下信息：

```
**** Installation completed successfully******
 
Additional information:
 *File /root/keystonerc_admin has been created on OpenStack client host10.0.30.51. To use the command line tools you need to source the file.
 * Toaccess the OpenStack Dashboard browse to http://10.0.30.51/dashboard .
Please, find your login credentials storedin the keystonerc_admin in your home directory.
```

到此就部署成功了，horizon登陆密码在 /root/keystonerc_admin 的export OS_PASSWORD参数中。 