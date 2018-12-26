# Devstack

安装教程：https://zhuanlan.zhihu.com/p/28996062

## 提示

当安装出错时，按照错误信息进行修改之后，最好先执行命令

```shell
./unstack.sh
```

再执行

```shell
./stack.sh
```



## 遇到的错误

1. 安装时发现brctl命令不存在，通过apt-get安装

```shell
sudo apt install bridge-utils
```



2. 从git上拉取ceilometer失败

```
git call failed: [git clone https://git.openstack.org/openstack/ceilometer /opt/stack/ceilometer --branch master]
```

因为https的端口号与http有所不同，需要关闭防火墙使git拉取顺利

```shell
sudo ufw disable
```



3. pip安装失败

```
2018-06-06 12:46:18.554 | curl: (52) Empty reply from server
2018-06-06 12:46:18.566 | + tools/install_pip.sh:install_get_pip:89  :   die 89 'Download of get-pip.py failed'
2018-06-06 12:46:18.568 | + functions-common:die:187                 :   local exitcode=52
2018-06-06 12:46:18.570 | [Call Trace]
2018-06-06 12:46:18.570 | /home/controller/devstack/tools/install_pip.sh:140:install_get_pip
2018-06-06 12:46:18.570 | /home/controller/devstack/tools/install_pip.sh:89:die
2018-06-06 12:46:18.574 | [ERROR] /home/controller/devstack/tools/install_pip.sh:89 Download of get-pip.py failed
2018-06-06 12:46:19.587 | ++./stack.sh:main:755                       err_trap
2018-06-06 12:46:19.597 | ++./stack.sh:err_trap:551                   local r=52
2018-06-06 12:46:19.605 | stack.sh failed: full log in /opt/stack/logs/stack.sh.log.2018-06-06-203400
2018-06-06 12:46:19.607 | Error on exit
```

手动安装pip

```
sudo apt-get install python-pip
```



4. 重复创建安全组default

```
2018-06-06 15:56:16.924 | Running user script /home/controller/devstack/local.sh
2018-06-06 15:56:16.930 | +./stack.sh:main:1390                      /home/controller/devstack/local.sh
2018-06-06 15:56:17.852 | WARNING: setting legacy OS_TENANT_NAME to support cli tools.
2018-06-06 15:56:17.865 | WARNING: setting legacy OS_TENANT_NAME to support cli tools.
2018-06-06 15:56:23.051 | +----------------------------+----------+
2018-06-06 15:56:23.051 | | Field                      | Value    |
2018-06-06 15:56:23.051 | +----------------------------+----------+
2018-06-06 15:56:23.051 | | OS-FLV-DISABLED:disabled   | False    |
2018-06-06 15:56:23.051 | | OS-FLV-EXT-DATA:ephemeral  | 0        |
2018-06-06 15:56:23.052 | | disk                       | 0        |
2018-06-06 15:56:23.052 | | id                         | 6        |
2018-06-06 15:56:23.052 | | name                       | m1.micro |
2018-06-06 15:56:23.052 | | os-flavor-access:is_public | True     |
2018-06-06 15:56:23.052 | | properties                 |          |
2018-06-06 15:56:23.052 | | ram                        | 128      |
2018-06-06 15:56:23.052 | | rxtx_factor                | 1.0      |
2018-06-06 15:56:23.052 | | swap                       |          |
2018-06-06 15:56:23.052 | | vcpus                      | 1        |
2018-06-06 15:56:23.052 | +----------------------------+----------+
2018-06-06 15:56:25.113 | More than one SecurityGroup exists with the name 'default'.
2018-06-06 15:56:27.153 | More than one SecurityGroup exists with the name 'default'.
2018-06-06 15:56:27.242 | ++./stack.sh:main:1390                      err_trap
2018-06-06 15:56:27.253 | ++./stack.sh:err_trap:551                   local r=1
2018-06-06 15:56:27.266 | stack.sh failed: full log in /opt/stack/logs/stack.sh.log.2018-06-06-205330
```

关键问题

```
More than one SecurityGroup exists with the name 'default'.
```

方法：注释掉`devstack/local.sh`中几句关于创建default组的语句

参考：https://stackoverflow.com/questions/42270910/stack-shmain1351-devstack-stack-sh-fails



5. etcd-v3.1.10-linux-amd64.tar.gz下载失败而导致校验和出错

在自己的主机上下载，或在节点上通过wget下载，之后移入`devstack/files/`文件夹下。

wget https://github.com/coreos/etcd/releases/download/v3.1.7/etcd-v3.1.7-linux-amd64.tar.gz

（注：可能需要开代理下载）



6. "g-api did not start"

这个问题比较严重，试了好几种方法都无效，最终使用了完全重新安装的方法

```shell
./unstack.sh
./clean.sh
```

移除devstack文件夹

```shell
rm -rf devstack
```

重启系统后，重新按教程从头开始安装

参考：http://www.cnblogs.com/pinganzi/p/6218244.html

http://www.aboutyun.com/thread-22448-1-1.html



7. 其他一些问题，是由于过程中出错解决后未执行

```
./unstack.sh
```

导致的问题，需要注意。