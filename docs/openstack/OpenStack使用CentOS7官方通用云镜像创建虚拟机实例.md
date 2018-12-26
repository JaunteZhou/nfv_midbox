# OpenStack使用CentOS7官方通用云镜像创建虚拟机实例

[willblog_CSDN](https://blog.csdn.net/networken/article/details/80334111)

**实验环境：**

- OpenStack Queens社区版
- 1控制节点、1计算节点、1块存储节点
- 单网卡provider供应商网络模式

**操作系统版本**

```
[root@controller ~]# cat /etc/redhat-release 
CentOS Linux release 7.4.1708 (Core) 
[root@controller ~]# uname -sr               
Linux 4.16.3-1.el7.elrepo.x86_641234
```

# 1.下载qcow2格式的CentOS官方通用云[镜像](https://www.baidu.com/s?wd=%E9%95%9C%E5%83%8F&tn=24004469_oem_dg&rsv_dl=gh_pc_csdn)

执行环境变量（官网有说明）

```ruby
[root@controller ~]# . admin-openrc
```

下载CentOS云[镜像](https://www.baidu.com/s?wd=%E9%95%9C%E5%83%8F&tn=24004469_oem_dg&rsv_dl=gh_pc_csdn)：

```
wget http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1802.qcow2c
```

官方链接：<http://cloud.centos.org/centos/7/images>

# 2.上传[镜像](https://www.baidu.com/s?wd=%E9%95%9C%E5%83%8F&tn=24004469_oem_dg&rsv_dl=gh_pc_csdn)到Glance

```
[root@controller ~]# openstack image create "CentOS7-image" \
  --file CentOS-7-x86_64-GenericCloud-1802.qcow2c \
  --disk-format qcow2 --container-format bare \
  --public
+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| checksum         | c5e362d0fb6e367ab16a5fbbed2ec1ce                     |
| container_format | bare                                                 |
| created_at       | 2018-05-16T02:06:12Z                                 |
| disk_format      | qcow2                                                |
| file             | /v2/images/de63a620-43da-4325-9ed5-cce8e74451f0/file |
| id               | de63a620-43da-4325-9ed5-cce8e74451f0                 |
| min_disk         | 0                                                    |
| min_ram          | 0                                                    |
| name             | CentOS7-image                                        |
| owner            | 2059d5d40c6a4d4ea37e5a80aa46b891                     |
| protected        | False                                                |
| schema           | /v2/schemas/image                                    |
| size             | 394918400                                            |
| status           | active                                               |
| tags             |                                                      |
| updated_at       | 2018-05-16T02:06:26Z                                 |
| virtual_size     | None                                                 |
| visibility       | public                                               |
+------------------+------------------------------------------------------+1234567891011121314151617181920212223242526
```

查看上传的镜像

```
[root@controller ~]# openstack image list
+--------------------------------------+---------------+--------+
| ID                                   | Name          | Status |
+--------------------------------------+---------------+--------+
| de63a620-43da-4325-9ed5-cce8e74451f0 | CentOS7-image | active |
| d81e109c-acb0-4f65-b739-58b9595282e7 | cirros        | active |
+--------------------------------------+---------------+--------+
```



