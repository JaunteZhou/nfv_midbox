#!/usr/bin/python
# -*- coding: utf-8 -*-
#chain.py
import logging
logger = logging.getLogger(__name__)

from midbox import flows
from midbox.db import db_services
from midbox._config import TYPE_DOCKER, TYPE_OPENSTACK,IN_PORT,OUT_PORT
from midbox.southbound.openstack.openstack_services import getVmInterfacesNameInDataPlane
"""
para:
{
    "func_ids": "xxxxxxxx-yyyyyyyy-zzzzzzzzz",
    "match_field": "",
    "priority": INT,
    "chain_id": "xxxxxxxx"
}
"""
#TODO:添加上层参数出错处理。（如match_field不合法：检查ovs返回信息，若为空则说明合法）
# 返回值：返回值为tuple，包含一个指示执行结果的值（0成功，1失败）和字符串。
def setChain(para):
    #必须初始化这两个端口名为有效的名称
    if IN_PORT=='default' or OUT_PORT=='default':
        return [1,"Error: Physical port name has not been initialized"]
    logger.debug('Start.')
    # function ids
    ids = para["func_ids"]
    # match field
    matchfield = para["match_field"] 
    # priority of flow_table
    priority = para["priority"]
    # chain id
    id = para["chain_id"]

    db,cursor=db_services.connect_db()
    id_list=ids.split('-')
    port_names_temp={0:("phy","phy")}
    
    if not __checkValid(db,cursor,id_list):
        return [1,"'Error:Function(s) don't  exist."]
    
    for i in id_list:
        func_type = db_services.select_table(db, cursor, "t_function", "type", i)
        # 获得虚拟机端口名的方法
        if func_type == TYPE_DOCKER:
            port_names_temp[i]=("br-c"+i+"-in","br-c"+i+"-out")
        elif func_type == TYPE_OPENSTACK:
            func_local_id = db_services.select_table(db, cursor, "t_function", "func_local_id", i)
            port_names_temp[i] = getVmInterfacesNameInDataPlane(func_local_id)
        else:
            return [1,"Error:Function don't have correct type"]
    
    n = 0
    flag = 0
    #list结尾附一个0，使得循环达到最后一个功能时n+1不会溢出
    id_list.append('0')
    while 1:
        if n==len(id_list)-1:
            aft = 0
            break
        __addRefCount(db,cursor,id_list[n])
        bef = 0
        aft = 0        
        if flag == 0:
            bef = 0
            flag = 1
        else:
            bef = id_list[n-1]
        if __diffHost(db,cursor,id_list[n],id_list[n+1]):
            aft = 0
            flag = 0
        else:
            aft=id_list[n+1]
        
        host_id = db_services.select_table(db, cursor, "t_function", "host_id", id_list[n])
        ip = db_services.select_table(db,cursor,"t_host","ip",host_id)
        password = db_services.select_table(db,cursor,"t_host","pwd",host_id)
        port_names = [port_names_temp[bef][0],port_names_temp[bef][1],\
            port_names_temp[id_list[n]][0],port_names_temp[id_list[n]][1],\
            port_names_temp[aft][0],port_names_temp[aft][1]]
                
        flows.flowDeploy(ip,password,port_names,\
            str(priority),matchfield,IN_PORT,OUT_PORT)
        n=n+1
    db_services.insert_flow(db,cursor,id,ids,matchfield)
    db_services.close_db(db,cursor)
    return [0,"Function Chain set completed,id:"+str(id)]



"""
para:
{
    "chain_id": "xxxxxxx"
}
"""
def delChain(para):
    #必须初始化这两个端口名为有效的名称
    if IN_PORT=='default' or OUT_PORT=='default':
        return [1,"Error: Physical port name has not been initialized"]
    logger.debug('Start.')
    #chain's id
    chain_id=para['chain_id']

    db,cursor=db_services.connect_db()
    id_list=db_services.select_table(db,cursor,"t_flow","chain", chain_id)
    id_list=id_list.split('-')
    port_names_temp={0:("phy","phy")}
    
    if not __checkValid(db,cursor,id_list):
        return [1,"Error:Container(s) don't  exist."]
    matchfield=db_services.select_table(db,cursor,"t_flow","match_field", chain_id)
    n=0
    flag=0
    
    for i in id_list:
        func_type = db_services.select_table(db,cursor,"t_function","type", i)
        if func_type == TYPE_DOCKER:
            port_names_temp[i]=("br-c"+i+"-in","br-c"+i+"-out")
        elif func_type == TYPE_OPENSTACK:
            func_local_id = db_services.select_table(db, cursor, "t_function", "func_local_id", i)
            port_names_temp[i] = getVmInterfacesNameInDataPlane(func_local_id)
            pass
        else:
            return [1,"Error:Function don't have correct type"]
    
    #同上
    id_list.append('0')
    while 1:
        if n==len(id_list)-1:
            aft=0
            break
        err=__decRefCount(db,cursor,id_list[n])
        if err<0:
            return [1,"Error:over deleted"]
        elif err==1:
            shutdownflag=1
        else:
            shutdownflag=0
        bef=0
        
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
        
        flows.flowUndeploy(ip,password,port_names,str(shutdownflag),matchfield,IN_PORT)
        n=n+1
    db_services.delete_table(db,cursor,"t_flow", chain_id)
    db_services.close_db(db,cursor)
    return [0,"Docker function chain deleted complete."]


def __checkValid(db,cursor,id_list):
    for id in id_list:
        if db_services.select_table(db,cursor,"t_function","host_id",id)=="None":
            return False
    return True

def __addRefCount(db,cursor,id): 
    refcount=db_services.select_table(db,cursor,"t_function","ref_count",id)
    db_services.update_table(db,cursor,"t_function","ref_count",refcount+1,id)
    return 0

def __diffHost(db,cursor,id1,id2):
    if db_services.select_table(db,cursor,"t_function","host_id",id1) != \
        db_services.select_table(db,cursor,"t_function","host_id",id2):
        return True
    else:
        return False

def __decRefCount(db,cursor,id): 
    refcount=db_services.select_table(db,cursor,"t_function","ref_count",id)
    if refcount<0:
        return -1
    db_services.update_table(db,cursor,"t_function","ref_count",refcount-1,id)
    if refcount==0:
        return 1
    return 0