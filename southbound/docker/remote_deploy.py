#!/usr/bin/python3
# -*- coding: utf-8 -*-
#remote_deploy.py

#暂未添加ssh管理接口,若要添加，直接连接至主机交换机即可
#关于任何一步出错反馈的处理，最终需考虑到。（改成每个Popen单独执行一条命令然后捕捉返回值？）

import time
import re
import sys
from remote_ssh import *

#ip:host ip;password:host password; cpu:cpu percents the container used(can be over 100); mem:memory used by the container; 
#image name:the image's name used to create a container; containerid:the id number of the NF,assigned by the upper layer
#cip:the ip address of the NF,assigned by the upper layer,should be with mask code;
def container_deploy(ip,password,cpu,mem,image_name,containerid,cip='192.168.1.1/24'):
    cpu=str(int(int(cpu)/100*1000000))
    print(containerid)
    mem=str(mem)

    args='docker run -d -m '+mem+'M -v /home/dockertest/:/data --cap-add=NET_ADMIN --cpu-period=1000000 --cpu-quota='+cpu+' --net=none --name c'+containerid+' '+image_name+' '
    exitstatus,rdata=remote_ssh(ip,password,args)
    exitstatus,rdata=remote_ssh(ip,password,'pid=$(docker inspect -f \'{{.State.Pid}}\' c'+containerid+') && mkdir -p /var/run/netns && ln -s /proc/$pid/ns/net /var/run/netns/$pid && echo $pid')
    pid=str(rdata);
    pid=re.findall('\d+',pid)[0]
    print('PID:'+pid)

    exitstatus,rdata=remote_ssh(ip,password,'ip link add in type veth peer name br-c'+containerid+'-in && ip link add out type veth peer name br-c'+containerid+'-out')
    exitstatus,rdata=remote_ssh(ip,password,'ip link set in netns '+pid+' && ip link set out netns '+pid+' && ip link set br-c'+containerid+'-in up && ip link set br-c'+containerid+'-out up')
    exitstatus,rdata=remote_ssh(ip,password,'ip netns exec '+pid+' ip link set in up && ip netns exec '+pid+' ip link set out up')
    exitstatus,rdata=remote_ssh(ip,password,'docker exec c'+containerid+' ovs-vsctl add-br sw && docker exec c'+containerid+' ovs-vsctl add-port sw in &&docker exec c'+containerid+' ovs-vsctl add-port sw out')#容器内网络配置

    #注意：容器镜像内必须安装OVS2.9以上版本！！
    exitstatus,rdata=remote_ssh(ip,password,' ifconfig br-c'+containerid+'-in down && ovs-vsctl add-port sw1 br-c'+containerid+'-in && ovs-vsctl add-port sw1 br-c'+containerid+'-out')#断掉回路，等容器启用时再up该接口
    exitstatus,rdata=remote_ssh(ip,password,'ip link add ceth0 type veth peer name br-c'+containerid+' && ip link set ceth0 netns '+pid+' && ip link set br-c'+containerid+' up')
    exitstatus,rdata=remote_ssh(ip,password,'ovs-vsctl add-port sw-man br-c'+containerid+' && ip netns exec '+pid+' ip link set ceth0 up && docker exec c'+containerid+' ifconfig ceth0 '+cip+' up')
    return 0


if __name__=='__main__':
    cpu=20#input('Input cpu limitation(%)(single core, if container uses mutiple cores, this value can larger than 100):');
    mem=128#input('Input memory limitation(MB):');
    image_name='testimage'
    containerid=sys.argv[1]
    ip='127.0.0.1'
    password='123456'
    container_deploy(ip,password,cpu,mem,image_name,containerid)


