# OpenStack问题

## 安装问题

### 问题0 [ You are using pip version 9.0.3, however version 10.0.1 is available. ]

#### 一、问题描述

```shell
"You are using pip version 9.0.3, however version 10.0.1 is available. You should consider upgrading via the 'pip install --upgrade pip' command."
```

#### 二、解决方案

若按照提示升级，确实可以成功（可能需要管理员权限），但是再次安装stack还是会出现这个问题。根本原因就不是pip版本的问题，而是要去关注其他出问题的原因。

### 问题1 [ etcd-v3.2.17-linux-amd64.tar.gz could not be downloaded ]

#### 一、问题描述

无法下载etcd-v3.2.17-linux-amd64.tar.gz文件

```shell
++functions:get_extra_file:67               [[ 4 -ne 0 ]]
++functions:get_extra_file:68               die 'https://github.com/coreos/etcd/releases/download/v3.2.17/etcd-v3.2.17-linux-amd64.tar.gz could not be downloaded'
++functions-common:die:187                  local exitcode=0
[ERROR] /opt/stack/devstack/functions:https://github.com/coreos/etcd/releases/download/v3.2.17/etcd-v3.2.17-linux-amd64.tar.gz could
+lib/etcd3:install_etcd3:101               etcd_file='[Call Trace]
./stack.sh:820:install_etcd3
/opt/stack/devstack/lib/etcd3:101:get_extra_file
/opt/stack/devstack/functions:68:die'
+lib/etcd3:install_etcd3:1                 exit_trap
```

#### 二、原因分析

偶尔网络的不通导致下载失败

#### 三、解决方案

多次重试`./stack.sh`或者手动下载文件之后放置到`~/devstack/files/`目录下。

#### 四、其他资料

[devstack-bugs](https://bugs.launchpad.net/devstack/+bug/1708631)

### 问题2 [ '/opt/stack/.cache/pip' or its parent directory is not owned by the current user ]

#### 一、问题描述

![屏幕快照 2018-12-08 16.25.49](/Users/JaunteZhou/Desktop/屏幕快照 2018-12-08 16.25.49.png)

```shell
The directory '/opt/stack/.cache/pip' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory.
```

#### 二、解决方案

为'/opt/stack/.cache/pip'目录添加权限，最好再修改所属用户

```shell
$ sudo chown -R stack:stack /opt/stack/
```

### 问题3 [ env: ‘/opt/stack/requirements/.venv/bin/pip’: No such file or directory ]

#### 一、问题描述

在devstack目录下运行 ./stack.sh ，出现错误描述：

```shell
+inc/python:pip_install:359
env http_proxy= https_proxy= no_proxy= PIP_FIND_LINKS= SETUPTOOLS_SYS_PATH_TECHNIQUE=rewrite /opt/stack/requirements/.venv/bin/pip install -c /opt/stack/requirements/upper-constraints.txt -U pbr
env: ‘/opt/stack/requirements/.venv/bin/pip’: No such file or directory
```

#### 二、解决方案

之后在stack用户下：

```shell
/opt/stack/devstack $ virtualenv ../requirements/.venv/
```

#### 三、参考资料

[Bwerf-AskUbuntu](https://askubuntu.com/questions/1040238/openstack-devstack-installation-ubuntu-16-04)

#### 四、其他资料

[安心smile-CSDN](https://blog.csdn.net/ANXIN997483092/article/details/81365588)

### 问题4 [ ContextualVersionConflict : xxxxxx x.x.x ]

#### 一、问题描述

```shell
2017-03-21 17:32:38.075 |     needed = self.resolve(parse_requirements(requirements))
2017-03-21 17:32:38.075 |   File "/usr/local/lib/python2.7/dist-packages/pip/_vendor/pkg_resources/__init__.py", line 859, in resolve
2017-03-21 17:32:38.075 |     raise VersionConflict(dist, req).with_context(dependent_req)
2017-03-21 17:32:38.075 | ContextualVersionConflict: (keystoneauth1 2.4.3 (/usr/local/lib/python2.7/dist-packages), Requirement.parse('keystoneauth1>=2.16.0'), set(['castellan']))
2017-03-21 17:32:38.198 | +inc/python:pip_install:1                  exit_trap
```

#### 二、解决方案

手动使用`pip install --upgrade keystoneauth1`进行升级，其他ContextualVersionConflict也用同样的方法处理；但若多个组件出现这样的安装问题，可能需要重新寻找解决方法。

### 问题5 [ ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out. ]

#### 一、问题描述

```shell
ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.
```

#### 二、原因分析

网络原因导致连接池失败，多次尝试即可。

#### 三、解决方案

再次运行`./stack.sh`

#### 四、其他资料

以下有两个方案提出的是修改timeout值

[Ateeb-stackoverflow](https://stackoverflow.com/questions/43298872/how-to-solve-readtimeouterror-httpsconnectionpoolhost-pypi-python-org-port)

[上官瑾文-云栖社区](https://yq.aliyun.com/articles/619208)

## 运行问题

### 问题1 [ Host 'HOST-NAME' is not mapped to any cell ]

#### 一、问题描述

```
错误 实例 "test-0" 执行所请求操作失败，实例处于错误状态。: 请稍后再试 [错误: Host 'HOST-NAME' is not mapped to any cell].
```

#### 二、原因分析

计算节点状态未更新至控制节点，在控制节点执行以下命令来发现所有的计算节点

```shell
# nova-manage cell_v2 discover_hosts --verbose
```

注意：执行以上代码前，确认已经载入用户名密码等环境变量

```shell
# admin-openrc.sh
export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://10.1.1.18/identity
```

### 问题2 [ 错误：创建端口 "" 失败。 ]

#### 一、问题描述

OpenStack界面显示：「 错误：创建端口 "" 失败。 」

#### 二、原因分析

可能是选择的用户或者项目的原因，demo项目似乎无法创建端口。但若还是没有解决，需要查看neutron服务是否挂掉。

#### 三、解决方案

切换至admin，或者其他项目用户

### 问题3 [ 实例创建在尝试6次后失败 ]

#### 一、问题描述

```
错误： 实例 "centos-server-1" 执行所请求操作失败，实例处于错误状态。: 请稍后再试 [错误: Build of instance 1518a018-b822-48fb-be1a-3a89e4c32112 aborted: Volume c04ac181-5ef2-46e9-bf64-e304ceda00a0 did not finish being created even after we waited 15 seconds or 6 attempts. And its status is error.].
```

#### 二、原因分析

分配的磁盘过小，无法安装虚拟机

#### 三、解决方案

创建虚拟机实例时，分配足够的磁盘空间

### 问题4 [ OpenStack删除Cinder盘失败解决办法 ]

#### 一、重启cinder服务

在删除磁盘时偶有发生，最初的原因为cinder服务DOWN掉了，需要重新启动cinder服务。（使用devstack安装openstack的前提下）

- 查看当前cinder服务状态

```shell
$ cinder service-list
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+
| Binary           | Host                   | Zone | Status  | State | Updated_at                 | Disabled Reason |
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+
| cinder-scheduler | controller             | nova | enabled | up    | 2018-07-26T05:10:29.000000 | -               |
| cinder-volume    | compute1@lvmdriver-1   | nova | enabled | down  | 2018-07-26T02:30:46.000000 | -               |
| cinder-volume    | compute2@lvmdriver-1   | nova | enabled | down  | 2018-07-09T13:15:06.000000 | -               |
| cinder-volume    | compute3@lvmdriver-1   | nova | enabled | down  | 2018-07-09T13:15:08.000000 | -               |
| cinder-volume    | controller@lvmdriver-1 | nova | enabled | up    | 2018-07-26T05:10:29.000000 | -               |
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+

```

- 查看cinder日志（/var/log/syslog）得到以下信息

```
ERROR cinder.volume.manager Stderr: u'  Volume group "stack-volumes-lvmdriver-1" not found\n  Cannot process volume group stack-volumes-lvmdriver-1\n'
 
 ERROR cinder.utils [None req-21482c69-6adc-493c-9ef2-1dc000c32b92 None None] Volume driver LVMVolumeDriver not initialized
  
 ERROR cinder.volume.manager [None req-21482c69-6adc-493c-9ef2-1dc000c32b92 None None] Cannot complete RPC initialization because driver isn't initialized properly.: DriverNotInitialized: Volume driver not ready.
 
 ERROR cinder.service [None req-21482c69-6adc-493c-9ef2-1dc000c32b92 None None] Manager for service cinder-volume compute3@lvmdriver-1 is reporting problems, not sending heartbeat. Service will appear "down".
```

- 一种常见的错误情况为磁盘空间挂载失败，先查看cinder的volumes文件情况

```shell
# cd /opt/stack/data
# ls -lh
total 172K
drwxr-xr-x 5 openstack openstack 4.0K Jun 26 08:51 cinder
drwxr-xr-x 3 openstack openstack 4.0K Jun 26 08:55 neutron
drwxr-xr-x 4 openstack root      4.0K Jun 26 08:51 nova
-rw-r--r-- 1 openstack openstack  24G Jun 26 08:51 stack-volumes-default-backing-file
-rw-r--r-- 1 openstack openstack  24G Jul  9 21:13 stack-volumes-lvmdriver-1-backing-file
```

- 关联volume文件

```shell
# losetup /dev/loop0 stack-volumes-default-backing-file
# losetup /dev/loop1 stack-volumes-lvmdriver-1-backing-file
```

- 查看

```shell
# lsblk
NAME                                                                    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda                                                                     253:0    0  150G  0 disk 
├─vda1                                                                  253:1    0  134G  0 part /
├─vda2                                                                  253:2    0    1K  0 part 
└─vda5                                                                  253:5    0   16G  0 part [SWAP]
loop0                                                                     7:0    0   24G  0 loop 
loop1                                                                     7:1    0   24G  0 loop 
├─stack--volumes--lvmdriver--1-stack--volumes--lvmdriver--1--pool_tmeta 252:0    0   24M  0 lvm  
│ └─stack--volumes--lvmdriver--1-stack--volumes--lvmdriver--1--pool     252:2    0 22.8G  0 lvm  
└─stack--volumes--lvmdriver--1-stack--volumes--lvmdriver--1--pool_tdata 252:1    0 22.8G  0 lvm  
  └─stack--volumes--lvmdriver--1-stack--volumes--lvmdriver--1--pool     252:2    0 22.8G  0 lvm
```

- 重启cinder服务（devstack安装）

```shell
# service devstack@c-vol restart
```

- 再次查看cinder服务状态

```shell
$ cinder service-list
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+
| Binary           | Host                   | Zone | Status  | State | Updated_at                 | Disabled Reason |
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+
| cinder-scheduler | controller             | nova | enabled | up    | 2018-07-26T05:31:09.000000 | -               |
| cinder-volume    | compute1@lvmdriver-1   | nova | enabled | up    | 2018-07-26T05:31:05.000000 | -               |
| cinder-volume    | compute2@lvmdriver-1   | nova | enabled | up    | 2018-07-26T05:31:05.000000 | -               |
| cinder-volume    | compute3@lvmdriver-1   | nova | enabled | up    | 2018-07-26T05:31:03.000000 | -               |
| cinder-volume    | controller@lvmdriver-1 | nova | enabled | up    | 2018-07-26T05:31:09.000000 | -               |
+------------------+------------------------+------+---------+-------+----------------------------+-----------------+
```

通过以上方法可以成功重启cinder服务，而僵尸卷依旧无法删除，因此搜索得到了以下方法

#### 二、删除僵尸卷

转载 [OpenStack删除Cinder盘失败解决办法 - Mr_扛扛 - CSDN](https://blog.csdn.net/u011521019/article/details/55854690)

##### 1、写在前面

这篇文章主要介绍了OpenStack cinder vloume在dashboard删除时出现删除错误或者一直在删除状态下的处理方式，由于作者（Mr_扛扛）能力或者理解不够透彻或许不是最好的方式，如果错误请告知， 如果转载，请保留作者信息。 
邮箱地址：jpzhang.ht@gmail.com 
个人博客：https://jianpengzhang.github.io/ 
CSDN博客：http://blog.csdn.net/u011521019

##### 2、问题

Openstack Cinder云硬盘，无法删除对应的云硬盘，一直在删除中，或者删除提示报错为云硬盘的状态不是错误或者可用状态，这块云硬盘成为僵尸记录。

##### 3、思路

Cinder创建云硬盘，如果是本地存储，即通过lvm的方式在物理机上划分一块空间，整体思路是通过lvremove删除物理服务器上的云硬盘空间，在数据库中标记这条记录的状态为已删除。

1、针对lvm，可以用命令lvdisplay列出所有卷的信息，如果应用命令lvremove来删除相应的卷，提示要删除的卷正在使用中，使用命令lsof查看相应卷所占用的进程，然后kill这个进程； 
2、应用命令lvremove来删除相应的卷； 
3、进入元数据库，修改这条记录状态，标记为已删除；

##### 4、操作

1）通过lvdisplay |grep查询cinder对应的卷地址。

```shell
root@compute:~# lvdisplay | grep "8580f464-02e1-411c-bd94-a4af35e499a3"
  LV Path                /dev/cinder-volumes/volume-8580f464-02e1-411c-bd94-a4af35e499a3
  LV Name                volume-8580f464-02e1-411c-bd94-a4af35e499a3
```

2）通过lsof | grep查询占用cinder卷的端口

```shell
root@compute:~# lsof | grep "8580f464-02e1-411c-bd94-a4af35e499a3"
root@compute:~# kill-9 76568
```

3）通过lvremove删除相应的卷

```shell
root@compute:~# lvremove /dev/cinder-volumes/volume-8580f464-02e1-411c-bd94-a4af35e499a3
```

4）报错处理 

```
报错：device-mapper: remove ioctl on failed: Deviceor resource busy。设备繁忙
```

- 查看是否被打开：


```shell
root@compute:~# dmsetup info -c /dev/cinder-volumes/volume-8580f464-02e1-411c-bd94-a4af35e499a3
```

- 查看被谁打开：


```shell
root@compute:~# fuser -m /dev/cinder-volumes/volume-8580f464-02e1-411c-bd94-a4af35e499a3
```

查看是谁打开的，显示产用进程号

- 把占用设备的进程杀掉：


```shell
root@compute:~# kill -9 xxxx xxxx xxxx xxxx
```

- 重新执行上面验证的几个步骤，验证是否还有进程占用，如果看到open为0，表示现在没有进程占用，再执行lvremove删除相应的卷

5）验证是否已经删除

```shell
root@compute:~# lvdisplay | grep "8580f464-02e1-411c-bd94-a4af35e499a3"
```

6）进入云平台系统，更改需要删除云硬盘状态为“可用配额”，然后“删除云硬盘”，如果再界面上删除依旧没有执行成功或者依旧一直再删除中，就采用比较暴力的方式，修改云硬盘再数据库中的状态，因为此时云硬盘再存储设备（物理机）上已经删除了，仅仅还有数据库中还有该记录信息，但不能直接删除这条记录，数据库有外键依赖，而是要把cinder盘的deleted改成“1”,“1”即为删除，0为不删除。

- 进入数据库：


```shell
root@controller:~# mysql -uxxxx -p
```

- 选择数据库表


```mysql
use cinder;
```

- select找到出错的数据:

```mysql
select id, status, display_name from volumes where id='2d5d206d-0720-42aa-b178-3f3238177583';
```

- 修改数据库记录状体：

```mysql
select id, status, display_name from volumes where id='2d5d206d-0720-42aa-b178-3f3238177583';
```

#### 三、dashboard中显示卷使用量异常的问题

通过以上操作成功删除僵尸卷后，dashboard中显示卷使用量错误，依旧包含了僵尸卷的问题。该问题在一定程度上不影响cinder使用，但是会使能创建的卷的最大数量减少。

> [cinder中删除僵尸卷（error_deleting ）的方法 - 溜溜小哥 - CSDN](https://blog.csdn.net/gaoxingnengjisuan/article/details/20871731)
>
> 此时问题貌似已经解决，因为已经可以正确地执行cinder中命令，要删除的卷的记录也已经删除。但是这里还有个问题，默认的建立卷的最大数目为10，如果之前删除的僵尸卷的数目为1，但是此时当你建立卷的数目为9个时，再尝试建立新卷时，就会提示已经达到卷的数目的最大值。解决方法就是到cinder数据表中找到quota_usages，将其中in_use中的数据减少相应的删除的僵尸卷的数目即可。

以此为思路搜索“cinder quota_usages”找到一篇写nova使用量异常的问答：

> [How to reset incorrect quota count? - ikke - AskOpenstack](https://ask.openstack.org/en/question/494/how-to-reset-incorrect-quota-count/)
>
> I noticed the count was wrong in the nova table in database. The fix that helped was that I set it manually to '-1' to force nova to recount the cpus:
>
> ```
> mysql -u nova -p<password> nova
> select * from quota_usages;
> update quota_usages set in_use='-1' where project_id='<my project id>';
> ```
>
> After I started a new instance, I was able to run it and quota numbers got updated!
>
> UPDATE for Icehouse: It's not -1 any longer, but 0 instead.
>
> ```
> update quota_usages set in_use='0' where project_id='<my project id>';
> ```

然后在自己的服务器上尝试：

- 首先在控制节点上进入mysql数据库

```shell
root@controller:~# mysql -uroot -p
```

- 切换到cinder数据库，并查询quota_usages表（最初使用`select * from quota_usages`进行查询，下面进行了优化）

```mysql
mysql> use cinder;
mysql> select id, project_id, resource, in_use from quota_usages;
+----+----------------------------------+-----------------------+--------+
| id | project_id                       | resource              | in_use |
+----+----------------------------------+-----------------------+--------+
|  1 | 6f11bc013f4b47b8bc6dc43381231e57 | gigabytes             |      0 |
|  2 | 6f11bc013f4b47b8bc6dc43381231e57 | gigabytes_lvmdriver-1 |      0 |
|  3 | 6f11bc013f4b47b8bc6dc43381231e57 | volumes_lvmdriver-1   |      0 |
|  4 | 6f11bc013f4b47b8bc6dc43381231e57 | volumes               |      0 |
|  5 | 4aacd0ec28824f50a6720c7c977b1be5 | gigabytes             |     17 |
|  6 | 4aacd0ec28824f50a6720c7c977b1be5 | gigabytes_lvmdriver-1 |     17 |
|  7 | 4aacd0ec28824f50a6720c7c977b1be5 | volumes_lvmdriver-1   |      3 |
|  8 | 4aacd0ec28824f50a6720c7c977b1be5 | volumes               |      3 |
|  9 | e922a17e84cc4b8e83a9ea441a650c0e | gigabytes             |     12 |
| 10 | e922a17e84cc4b8e83a9ea441a650c0e | gigabytes_lvmdriver-1 |     12 |
| 11 | e922a17e84cc4b8e83a9ea441a650c0e | volumes_lvmdriver-1   |      3 |
| 12 | e922a17e84cc4b8e83a9ea441a650c0e | volumes               |      3 |
+----+----------------------------------+-----------------------+--------+
```

- 根据dashboard中查看到的project_id为e922a17e84cc4b8e83a9ea441a650c0e，项目当前使用卷实际为1个=1G，两个僵尸卷分别为1G和10G，因而数据库中显示3个=12G，所以我使用以下数据库命令进行修改。

```mysql
mysql> update quota_usages set in_use='1' where project_id='e922a17e84cc4b8e83a9ea441a650c0e';
```

实际建议使用4条指令分别修改：

```mysql
mysql> update quota_usages set in_use='<usage>' where project_id='<project_id>' and resource='gigabytes';
mysql> update quota_usages set in_use='<usage>' where project_id='<project_id>' and resource='gigabytes_lvmdriver-1';
mysql> update quota_usages set in_use='<usage>' where project_id='<project_id>' and resource='volumes_lvmdriver';
mysql> update quota_usages set in_use='<usage>' where project_id='<project_id>' and resource='volumes';
```

- 再次查看数据库

```mysql
mysql> select id, project_id, resource, in_use from quota_usages;
+----+----------------------------------+-----------------------+--------+
| id | project_id                       | resource              | in_use |
+----+----------------------------------+-----------------------+--------+
|  1 | 6f11bc013f4b47b8bc6dc43381231e57 | gigabytes             |      0 |
|  2 | 6f11bc013f4b47b8bc6dc43381231e57 | gigabytes_lvmdriver-1 |      0 |
|  3 | 6f11bc013f4b47b8bc6dc43381231e57 | volumes_lvmdriver-1   |      0 |
|  4 | 6f11bc013f4b47b8bc6dc43381231e57 | volumes               |      0 |
|  5 | 4aacd0ec28824f50a6720c7c977b1be5 | gigabytes             |     17 |
|  6 | 4aacd0ec28824f50a6720c7c977b1be5 | gigabytes_lvmdriver-1 |     17 |
|  7 | 4aacd0ec28824f50a6720c7c977b1be5 | volumes_lvmdriver-1   |      3 |
|  8 | 4aacd0ec28824f50a6720c7c977b1be5 | volumes               |      3 |
|  9 | e922a17e84cc4b8e83a9ea441a650c0e | gigabytes             |      1 |
| 10 | e922a17e84cc4b8e83a9ea441a650c0e | gigabytes_lvmdriver-1 |      1 |
| 11 | e922a17e84cc4b8e83a9ea441a650c0e | volumes_lvmdriver-1   |      1 |
| 12 | e922a17e84cc4b8e83a9ea441a650c0e | volumes               |      1 |
+----+----------------------------------+-----------------------+--------+
```

确认修改完成，并且dashboard上也显示正确。