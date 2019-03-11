#!/usr/bin/python
# -*- coding: utf-8 -*-
#flows.py
import logging
logger = logging.getLogger(__name__)

# import time
# import re
from midbox.southbound.docker.remote_ssh import remote_ssh

#ip:物理机ip地址 password：物理机密码 port_names:包含三个服务功能主体的共六个网卡名，若有物理网卡则出入口名称相同均为“phy” phy_in:物理机流量入口名 phy_out：物理机流量出口名 match_field：流匹配域（不含in_port） priority:优先级
#以上参数全部为字符串
#out_id应为一组id
def flowDeploy(ip, password, port_names, priority='1', 
            match_field="", phy_in="ens7", phy_out="ens8"):  
    logger.debug('Start.')

    if match_field != '':
        match_field = ','+match_field
    if port_names[0] != "phy":
        ret = addOvsFlow(ip, password, "sw1", 
                priority, port_names[1], match_field, "output:"+port_names[2])
        # exit,rdata=remote_ssh(ip, password,
        #         "ovs-ofctl add-flow sw1 "+"priority="+priority+",in_port="+port_names[1]+match_field+",actions=output:"+port_names[2])  
        # logger.info(rdata);
    else:
        ret = addOvsFlow(ip, password, "sw1", 
                priority, phy_in, match_field, "output:"+port_names[2])
        # exit,rdata=remote_ssh(ip, password,
        #         "ovs-ofctl add-flow sw1 priority="+priority+",in_port="+phy_in+match_field+",actions=output:"+port_names[2])
        # logger.info(rdata);
    if port_names[4] == "phy":
        ret = addOvsFlow(ip, password, "sw1", 
                priority, port_names[3], match_field, "output:"+phy_out)
        # exit,rdata=remote_ssh(ip, password,
        #         "ovs-ofctl add-flow sw1 priority="+priority+",in_port="+port_names[3]+match_field+",actions=output:"+phy_out)
        # logger.info(rdata);
    else:
        ret = addOvsFlow(ip, password, "sw1", 
                priority, port_names[3], match_field, "output:"+port_names[4])
        # exit,rdata=remote_ssh(ip, password,
        #         'ovs-ofctl add-flow sw1 priority='+priority+',in_port='+port_names[3]+match_field+',actions=output:'+port_names[4])
        # logger.info(rdata);

    exit = ret[0]
    rdata = ret[1]
    logger.info((port_names[0], port_names[4], rdata));
    #不再需要drop，只需保证OVS无NORMAL流表项即可，注释此行，确定无误后删除
    #exit,rdata=remote_ssh(ip,password,'ovs-ofctl add-flow sw1 in_port='+port_names[2]+',actions=drop && ifconfig '+port_names[2]+' up')
    exit,rdata=remote_ssh(ip,password,'ifconfig '+port_names[2]+' up')
    logger.info(rdata);
    return 0

def addOvsFlow(ip, password, sw, priority, in_port, match_field, actions):
    exit,rdata = remote_ssh(ip, password,
            "ovs-ofctl add-flow "+sw+" priority="+priority+",in_port="+in_port \
            +match_field+",actions="+actions)
    logger.info((in_port, actions, rdata));
    return [exit, rdata]


#ip:物理机ip地址 password：物理机密码 port_names:包含两个功能共四个网卡名，若有物理网卡则出入口名称相同均为“phy_in/phy_out” shutdown_flag:指示当前容器是否没有被任何功能链使用 phy_in:物理机流量入口名 match_field：流匹配域 
#以上参数全部为字符串
#shutdown_flag将由容器类的引用计数判断
def flowUndeploy(ip, password, port_names, shutdown_flag, match_field="", phy_in="ens7"):
    logger.debug('Start.')
    
    if match_field != '':
        match_field = ','+match_field
    if shutdown_flag == "1":
        exit,rdata = remote_ssh(ip, password, 'ifconfig '+port_names[2]+' down')
        logger.info(rdata);
    if port_names[0]!="phy":
        ret = delOvsFlow(ip, password, "sw1", port_names[1], match_field)
        # exit,rdata=remote_ssh(ip, password,
        #         "ovs-ofctl del-flows sw1 "+"in_port="+port_names[1]+match_field)
        logger.info(ret);
    else:
        ret = delOvsFlow(ip, password, "sw1", phy_in, match_field)
        # exit,rdata=remote_ssh(ip, password,
        #         "ovs-ofctl del-flows sw1 in_port="+phy_in+match_field)
        logger.info(ret);
    ret = delOvsFlow(ip, password, "sw1", port_names[3], match_field)
    # exit,rdata=remote_ssh(ip, password,
    #         "ovs-ofctl del-flows sw1 "+"in_port="+port_names[3]+match_field)
    logger.info(ret);
    
    return 0

def delOvsFlow(ip, password, sw, in_port, match_field):
    exit,rdata=remote_ssh(ip, password,
            "ovs-ofctl del-flows "+sw+"in_port="+in_port+match_field)
    logger.info(rdata);
    return [exit, rdata]


if __name__=='__main__':
    ip='127.0.0.1'
    password='123456'

    import sys
    in_id=sys.argv[1]
    cid=sys.argv[2]
    out_id=sys.argv[3]
    flowDeploy(ip,password,in_id,out_id,cid)

    # in_id=sys.argv[1]
    # cid=sys.argv[2]
    # flowUndeploy(ip,password,in_id,cid,'0')