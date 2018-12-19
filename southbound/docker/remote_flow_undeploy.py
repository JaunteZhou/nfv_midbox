#!/usr/bin/python3
# -*- coding: utf-8 -*-
#remote_flow_undeploy.py

import time
import re
import sys
from remote_ssh import *

#ip:物理机ip地址 password：物理机密码 port_names:包含两个功能共四个网卡名，若有物理网卡则出入口名称相同均为“phy_in/phy_out” shutdown_flag:指示当前容器是否没有被任何功能链使用 phy_in:物理机流量入口名 match_field：流匹配域 
#以上参数全部为字符串
#shutdown_flag将由容器类的引用计数判断
def flow_undeploy(ip,password,port_names,shutdown_flag,match_field="",phy_in="ens7"):
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
    flow_undeploy(ip,password,in_id,cid,'0')