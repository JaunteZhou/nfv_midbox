# 在Ubuntu16中使用devstack安装openstack

## 前言

起初，按照OpenStack官方文档[Documentation for Pike](https://docs.openstack.org/pike/)进行安装，但过程十分繁杂，且遇到了各种各样的环境配置问题，费时费力还不成功。之后，发现了[DevStack官方文档](https://docs.openstack.org/devstack/latest/)，通过脚本简化安装步骤，纵然过程中依旧会有环境配置问题，但解决起来更加方便，也整理了相关的问题集。

本文编写参考[Ubuntu16安装OpenStack - VoidKing - 简书](https://www.jianshu.com/u/9f179465dd2b)和[DevStack 安装 grizzly-eol 版本 OpenStack](http://ohmystack.com/articles/install-OpenStack-using-Devstack)

## 目标

本文的目标是搭建一个双节点OpenStack，所有核心服务都安装在控制节点上，节点IP为10.1.1.18；计算节点上只安装计算服务和磁盘服务等少量服务，节点IP为10.1.1.7。

核心服务包括：身份认证服务keystone，镜像服务glance，计算服务nova（默认使用KVM虚拟化），网络服务neutron，仪表板horizon。也需要包含一些支持服务，例如：SQL数据库，消息队列和NTP。

## 环境准备

操作系统：Ubuntu 16.04

文本编辑器：vim（可选vi / gedit等）

### 时间同步

1、同步时区
执行命令`sudo dpkg-reconfigure tzdata`，然后选择Asia，Shanghai。

2、安装时间同步工具

```
$ sudo apt-get install ntpdate
$ sudo ntpdate cn.pool.ntp.org
$ date
```

### 更换sources.list（可选）

参考[《Ubuntu更换源列表》](https://www.voidking.com/dev-ubuntu-change-sources/)。

1、备份源列表文件

```shell
$ sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

2、编辑源列表文件

```shell
$ sudo vim /etc/apt/sources.list
```

修改为：

```
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
```

3、更新资源包

```shell
$ sudo apt-get update
```

### 更换pip源（可选）

参考[《python pip更换国内源》](https://www.voidking.com/dev-pip-source/)。

1、安装python

```shell
$ sudo apt-get install python
```

2、创建pip.conf

```shell
$ mkdir ~/.pip && vim ~/.pip/pip.conf
```

写入内容如下：

```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host = http://mirrors.aliyun.com/pypi/simple/
```

## DevStack下载

1、安装git

```shell
$ sudo apt-get install git
```

2、下载devstack并切换到queens分支

```shell
$ git clone https://git.openstack.org/openstack-dev/devstack -b stable/rocky
```

## 创建stack用户

#### 方法一

1. 执行创建用户脚本

```shell
$ sudo devstack/tools/create-stack-user.sh
```

2. 将devstack目录放到/opt/stack中并设置权限

```shell
$ sudo mv devstack /opt/stack
$ sudo chown -R stack:stack /opt/stack
```

3. 切换到stack用户（必要步骤，不可在root权限下进行安装）

```shell
$ sudo su - stack
```

#### 方法二：

1. 添加stack用户
```shell
$ sudo useradd -s /bin/bash -d /opt/stack -m stack
```

2. 给stack用户添加sudo权限

```shell
$ echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
```

3. 将devstack目录放到/opt/stack中并设置权限

```shell
$ sudo mv devstack /opt/stack
$ sudo chown -R stack:stack /opt/stack
```

4. 切换到stack用户（之后的所有命令都在stack用户下执行）

```shell
$ sudo su - stack
```

## 编辑local.conf

拷贝local.conf

```shell
$ cd devstack
$ cp samples/local.conf ./
```

编辑local.conf参考DevStack文档[Guides - DevStack](https://docs.openstack.org/devstack/latest/guides.html)，并根据自身项目需求进行一定的修改。

本文参考使用的是[Using DevStack with neutron Networking - DevStack Doc](https://docs.openstack.org/devstack/latest/guides/neutron.html)。

## 编译安装

执行安装

```shell
$ ./stack.sh
```

### 再次安装

当编译安装过程中失败之后，通过对应的方式解决问题，再通过以下命令卸载和清空当前安装：

```shell
$ ./unstack.sh
$ ./clean.sh
```

之后，再次安装

```shell
$ ./stack.sh
```

若成功，则可以看到终端中显示已安装的OpenStack的一些基本信息。

## 安装完成后

打开浏览器，输入OpenStack的控制面板的URL，本文中为：

```http
10.1.1.18/dashboard
```

输入用户名密码，即可登录查看OpenStack的各项信息。

（注意：顶部栏中有用户选项和项目选项，很多功能必须在admin下才可以查看与更改）