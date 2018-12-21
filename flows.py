#!/usr/bin/python3
# -*- coding: utf-8 -*-
#flows.py

import time
import re
import sys
from nfv_midbox.southbound.docker.remote_ssh import remote_ssh

#ip:物理机ip地址 password：物理机密码 port_names:包含三个服务功能主体的共六个网卡名，若有物理网卡则出入口名称相同均为“phy” phy_in:物理机流量入口名 phy_out：物理机流量出口名 match_field：流匹配域（不含in_port） priority:优先级
#以上参数全部为字符串
#out_id应为一组id
def flowDeploy(ip,password,port_names,priority='1',match_field="",phy_in="ens7",phy_out="ens8"):  
    if match_field!='':
        match_field=','+match_field
    if port_names[0]!="phy":
        remote_ssh(ip,password,"ovs-ofctl add-flow sw1 "+"priority="+priority+",in_port="+port_names[1]+match_field+",actions=output:"+port_names[2])        
    else:
        remote_ssh(ip,password,"ovs-ofctl add-flow sw1 priority="+priority+",in_port="+phy_in+match_field+",actions=output:"+port_names[2])
    if port_names[4]=="phy":
        remote_ssh(ip,password,"ovs-ofctl add-flow sw1 priority="+priority+",in_port="+port_names[3]+match_field+",actions=output:"+phy_out)
    else:
        remote_ssh(ip,password,'ovs-ofctl add-flow sw1 priority='+priority+',in_port='+port_names[3]+match_field+',actions=output:'+port_names[4])
    remote_ssh(ip,password,'ovs-ofctl add-flow sw1 in_port='+port_names[2]+',actions=drop && ifconfig '+port_names[2]+' up')
    return 0


#ip:物理机ip地址 password：物理机密码 port_names:包含两个功能共四个网卡名，若有物理网卡则出入口名称相同均为“phy_in/phy_out” shutdown_flag:指示当前容器是否没有被任何功能链使用 phy_in:物理机流量入口名 match_field：流匹配域 
#以上参数全部为字符串
#shutdown_flag将由容器类的引用计数判断
def flowUndeploy(ip,password,port_names,shutdown_flag,match_field="",phy_in="ens7"):
    if match_field!='':
        match_field=','+match_field
    if shutdown_flag=="1":
        remote_ssh(ip,password,'ifconfig '+port_names[2]+' down')
    if port_names[0]!="phy":
        remote_ssh(ip,password,"ovs-ofctl del-flows sw1 "+"in_port="+port_names[1]+match_field)
    else:
        remote_ssh(ip,password,"ovs-ofctl del-flows sw1 in_port="+phy_in+match_field)
    remote_ssh(ip,password,"ovs-ofctl del-flows sw1 "+"in_port="+port_names[3]+match_field)
    
    return 0


if __name__=='__main__':
    ip='127.0.0.1'
    password='123456'

    in_id=sys.argv[1]
    cid=sys.argv[2]
    out_id=sys.argv[3]
    flowDeploy(ip,password,in_id,out_id,cid)

    # in_id=sys.argv[1]
    # cid=sys.argv[2]
    # flowUndeploy(ip,password,in_id,cid,'0')