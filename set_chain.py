#!/usr/bin/python3
# -*- coding: utf-8 -*-
#setChain.py
from southbound.docker import remote_flow_deploy
from db import db_services
from config import DOCKER_TYPE, OPENSTACK_TYPE
"""
para:
{
    "func_ids": "xxxxxxxx-yyyyyyyy-zzzzzzzzz",
    "match_field": "",
    "priority": INT,
    "chain_id": "xxxxxxxx"
}
"""
# 返回值：返回值为tuple，包含一个指示执行结果的值（0成功，1失败）和字符串。
def setChain(para):
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
        if func_type == DOCKER_TYPE:
            port_names_temp[i]=("br-c"+i+"-in","br-c"+i+"-out")
        elif func_type == OPENSTACK_TYPE:
            # TODO: 此处应有获得虚拟机端口名的方法
            pass
        else:
            return [1,"Error:Function don't have correct type"]
    
    n = 0
    flag = 0
    while 1:
        # TODO: 这个循环结束条件是什么？好像是死循环
        __addRefCount(db,cursor,id_list[n])
        bef = 0
        aft = 0
        if n==len(id_list):
            aft = 0
            break
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
                
        remote_flow_deploy.flow_deploy(ip,password,port_names,\
            str(priority),matchfield)
        n=n+1
    db_services.insert_flow(db,cursor,id,ids,matchfield)
    db_services.close_db(db,cursor)
    return [0,"Function Chain set completed,id:"+str(id)]

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