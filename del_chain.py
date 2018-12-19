#!/usr/bin/python3
# -*- coding: utf-8 -*-
#delChain.py
from db import db_services
from southbound.docker import remote_flow_undeploy
from config import DOCKER_TYPE, OPENSTACK_TYPE

"""
para:
{
    "chain_id": "xxxxxxx"
}
"""

def delChain(id):
    db,cursor=db_services.connect_db()
    id_list=db_services.select_table(db,cursor,"t_flow","flow",id)
    id_list=id_list.split('-')
    port_names_temp={0:("phy","phy")}
    
    if not __checkValid(db,cursor,id_list):
        return [1,"Error:Container(s) don't  exist."]
    matchfield=db_services.select_table(db,cursor,"t_flow","match_field",id)
    n=0
    flag=0
    
    for i in id_list:
        func_type = db_services.select_table(db,cursor,"t_function","type", i)
        if func_type == DOCKER_TYPE:
            port_names_temp[i]=("br-c"+i+"-in","br-c"+i+"-out")
        elif func_type == OPENSTACK_TYPE:
            # TODO: 此处应有获得虚拟机端口名的方法
            pass
        else:
            return [1,"Error:Function don't have correct type"]
    
    while 1:
        err=__decRefCount(db,cursor,id_list[n])
        if err<0:
            return [1,"Error:over deleted"]
        elif err==1:
            shutdownflag=1
        else:
            shutdownflag=0
        bef=0
        if n==len(id_list):
            aft=0
            break
        if flag==0:
            bef=0
            flag=1
        else:
            bef=id_list[n-1]
        if __diffHost(db,cursor,id_list[n],id_list[n+1]):
            flag=0
        host_id=db_services.select_table(db,cursor,"t_function","host_id",id_list[n])
        ip=db_services.select_table(db,cursor,"t_host","ip",host_id)
        password=db_services.select_table(db,cursor,"t_host","pwd",host_id)
        port_names=[port_names_temp[bef][0],port_names_temp[bef][1],\
            port_names_temp[id_list[n]][0],port_names_temp[id_list[n]][1]]
        
        remote_flow_undeploy.flow_undeploy(ip,password,port_names,str(shutdownflag),matchfield)
        n=n+1
    db_services.delete_table(db,cursor,"t_flow",id)
    db_services.close_db(db,cursor)
    return [0,"Docker function chain deleted complete."]



def __checkValid(db,cursor,id_list):
    for id in id_list:
        if db_services.select_table(db,cursor,"t_function","host_id",id)=="None":
            return False
    return True

def __decRefCount(db,cursor,id): 
    refcount=db_services.select_table(db,cursor,"t_function","ref_count",id)
    if refcount<0:
        return -1
    db_services.update_table(db,cursor,"t_function","ref_count",refcount-1,id)
    if refcount==0:
        return 1
    return 0

def __diffHost(db,cursor,id1,id2):
    if db_services.select_table(db,cursor,"t_function","host_id",id1)!= \
        db_services.select_table(db,cursor,"t_function","host_id",id2):
        return True
    else:
        return False

