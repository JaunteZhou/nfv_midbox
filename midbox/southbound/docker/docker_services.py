#!/usr/bin/python3
# -*- coding: utf-8 -*-
# docker_services.py

# 暂未添加ssh管理接口,若要添加，直接连接至主机交换机即可
# 关于任何一步出错反馈的处理，最终需考虑到。（改成每个Popen单独执行一条命令然后捕捉返回值？）

import re
import sys
import logging
from midbox.southbound.remote_ssh import *
from midbox._config import DOCKER_REGISTRY_IP, DOCKER_REGISTRY_PORT, CTRL_PLANE_SW_NAME, DATA_PLANE_SW_NAME


def addContainer(ip, password, cpu, mem, image_name, containerid, cip='192.168.1.1/24'):
    """
    部署Docker容器
    :param ip: 主机ip
    :param password: 主机管理员密码
    :param cpu: cpu百分比
    :param mem: 内存大小
    :param image_name: docker镜像名
    :param containerid: 上层分配给容器的id
    :param cip: 上层分配给功能实例的ip地址，附带网络掩码
    :return:
    """
    cpu=str(int(int(cpu)*1000000/100))
    mem=str(mem)
    image_name=DOCKER_REGISTRY_IP+':'+DOCKER_REGISTRY_PORT+'/'+image_name

    logger=logging.getLogger(__name__)

    args='docker run -d -m '+mem+'M -v /home/dockertest/:/data --cap-add=NET_ADMIN --cpu-period=1000000 --cpu-quota='+cpu+' --net=none --name c'+containerid+' '+image_name+' '
    exitstatus,rdata=remote_ssh(ip,password,args)
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'pid=$(docker inspect -f \'{{.State.Pid}}\' c'+containerid+') && mkdir -p /var/run/netns && ln -s /proc/$pid/ns/net /var/run/netns/$pid && echo $pid')
    logger.info(rdata);
    pid=rdata;
    pid=re.findall('\d+',pid)[0]
    print('PID:'+pid)

    exitstatus,rdata=remote_ssh(ip,password,'ovs-vsctl add-br sw1 && ovs-vsctl add-br sw-man')
    exitstatus,rdata=remote_ssh(ip,password,'ip link add in type veth peer name br-c'+containerid+'-in && ip link add out type veth peer name br-c'+containerid+'-out')
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'ip link set in netns '+pid+' && ip link set out netns '+pid+' && ip link set br-c'+containerid+'-in up && ip link set br-c'+containerid+'-out up')
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'ip netns exec '+pid+' ip link set in up && ip netns exec '+pid+' ip link set out up')
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'docker exec c'+containerid+' ovs-vsctl add-br sw && docker exec c'+containerid+' ovs-vsctl add-port sw in &&docker exec c'+containerid+' ovs-vsctl add-port sw out')#容器内网络配置
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'docker start c'+containerid)
    logger.info(rdata)

    #注意：容器镜像内必须安装OVS2.9以上版本！！
    exitstatus,rdata=remote_ssh(ip,password,' ifconfig br-c'+containerid+'-in down && ovs-vsctl add-port sw1 br-c'+containerid+'-in && ovs-vsctl add-port sw1 br-c'+containerid+'-out')#断掉回路，等容器启用时再up该接口
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'ip link add ceth0 type veth peer name br-c'+containerid+' && ip link set ceth0 netns '+pid+' && ip link set br-c'+containerid+' up')
    logger.info(rdata);
    exitstatus,rdata=remote_ssh(ip,password,'ovs-vsctl add-port sw-man br-c'+containerid+' && ip netns exec '+pid+' ip link set ceth0 up && docker exec c'+containerid+' ifconfig ceth0 '+cip+' up')
    logger.info(rdata);
    return 0


def delContainer(ip, password, containerid):
    """
    删除Docker容器实例
    # 暂未添加ssh管理接口,若要添加，直接连接至主机交换机即可
    # containerid应该每台宿主机可重复，与物理机id建立映射关系保证唯一性以及可计算得到（how to do？）
    # 关于任何一步出错反馈的处理，最终需考虑到。（改成每个Popen单独执行一条命令然后捕捉返回值？）
    # 考虑容器初始时没有启动两块网卡，只有当有效的流表下发后才启动，下发流表是单独的行为。
    :param ip: 主机ip
    :param password: 主机管理员密码
    :param containerid: 容器的id
    :return:
    """
    logger = logging.getLogger(__name__)

    exitstatus, rdata = remote_ssh(ip, password,
                                   'pid=$(docker inspect -f \'{{.State.Pid}}\' c' + containerid + ') && echo $pid')
    logger.info(rdata);
    pid = str(rdata)
    pid = re.findall('\d+', pid)[0]
    print('PID:' + pid)
    exitstatus, rdata = remote_ssh(ip, password,
                                   'docker stop c' + containerid + ' && docker rm c' + containerid + ' && rm -rf /var/run/netns/$' + pid)
    logger.info(rdata);
    exitstatus, rdata = remote_ssh(ip, password,
                                   'ovs-vsctl del-port sw1 br-c' + containerid + '-in && ovs-vsctl del-port sw1 br-c' + containerid + '-out && ovs-vsctl del-port sw-man br-c' + containerid)
    logger.info(rdata);

    return 0


if __name__ == '__main__':
    # 新增
    # input('Input cpu limitation(%)' +
    # '(single core, if container uses mutiple cores, this value can larger than 100):')
    cpu = 20
    mem = 128  # input('Input memory limitation(MB):')
    image_name = 'bimage'
    containerid = sys.argv[1]
    ip = '127.0.0.1'
    password = '123456'
    # container_deploy(ip, password, cpu, mem, image_name, containerid)

    # 删除
    # image_name=input('Input image name:')
    # containerid=input('Input container id:')
    containerid = sys.argv[1]
    ip = '127.0.0.1'
    password = '123456'
    # container_clear(ip, password, containerid)
