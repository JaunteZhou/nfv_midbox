#!/usr/bin/python3
# -*- coding: utf-8 -*-
#remote_clear.py

#image_name=input('Input image name:')
#containerid=input('Input container id:')
#暂未添加ssh管理接口,若要添加，直接连接至主机交换机即可
#containerid应该每台宿主机可重复，与物理机id建立映射关系保证唯一性以及可计算得到（how to do？）
#关于任何一步出错反馈的处理，最终需考虑到。（改成每个Popen单独执行一条命令然后捕捉返回值？）
#考虑容器初始时没有启动两块网卡，只有当有效的流表下发后才启动，下发流表是单独的行为。

import time
import re
import sys
import logging
from midbox.southbound.docker.remote_ssh import *

def container_clear(ip,password,containerid):
    logger=logging.getLogger(__name__)

    exitstatus,rdata=remote_ssh(ip,password,'pid=$(docker inspect -f \'{{.State.Pid}}\' c'+containerid+') && echo $pid')
    logger.info(rdata);
    pid=str(rdata)
    pid=re.findall('\d+',pid)[0]
    print('PID:'+pid)
    exitstatus,rdata=remote_ssh(ip,password,'docker stop c'+containerid+' && docker rm c'+containerid+' && rm -rf /var/run/netns/$'+pid)
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'ovs-vsctl del-port sw1 br-c'+containerid+'-in && ovs-vsctl del-port sw1 br-c'+containerid+'-out && ovs-vsctl del-port sw-man br-c'+containerid)
    logger.info(rdata);
    
    return 0


if __name__=='__main__':
    containerid=sys.argv[1]
    ip='127.0.0.1'
    password='123456'
    container_clear(ip,password,containerid)




