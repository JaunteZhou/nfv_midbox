#!/usr/bin/python3
# -*- coding: utf-8 -*-
#setContainer.py

import southbound.docker.remote_deploy
import db.db_services

#para:

#{
#    "func_type":"<container/vm>",
#    "func_id":"<上层分配的功能编号>",
#    "host_id":"<上层指定的部署位置>",
#    "image_id":"<功能使用的镜像id>",
#    "func_ip":"<上层为功能实体分配的ip地址>",
#    "func_pwd":"<功能实体ssh登录密码，若为容器则应使用默认密码>",
#    "cpu":"<功能使用的CPU情况，注意区分容器和虚拟机使用的不同单位>",
#    "mem":"<功能内存限制>"
#    "disk":"<功能硬盘容量限制，这个项目对容器是无效的>"
#}

def setFunction(para):
    db,cursor=db_services.connect_db()
    hostip=db_services.select_table(db,cursor,'t_host','ip',para['host_id'])
    if hostip==():#空tuple表示未查询到对应条目
        return [1,"Error: Host doesn't exist."]
    hostpwd=db_services.select_table(db,cursor,'t_host','pwd',para['host_id'])
    
    if para["func_type"]=="container":
        db_services.insert_function(db,cursor,para["func_id"],para["image_id"],para["host_id"],0,\
                              para["func_ip"],para["func_pwd"],para["cpu"],para["mem"],\
                              1,0,0)        
        imagename=db_services.select_table(db,cursor,'t_image','func',para['image_id'])
        remote_deploy.container_deploy(hostip,hostpwd,para['cpu'],para['mem'],imagename\
            ,para['func_id'],para['func_ip'])
    elif para["func_type"]=="vm":
        #TODO:此处创建虚拟机
        pass
    db_services.close_db(db,cursor)
    return[0,"Function Created Succesfully! IP:"+para['func_ip']];