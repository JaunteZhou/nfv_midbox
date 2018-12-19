#!/usr/bin/python3
# -*- coding: utf-8 -*-
#setContainer.py

import remote_docker.remote_deploy
import nfvdb

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
    db,cursor=nfvdb.connect_db()
    if para["func_type"]=="container":
        nfvdb.insert_function(db,cursor,para["func_id"],para["image_id"],para["host_id"],0,\
                              para["func_ip"],para["func_pwd"],para["cpu"],para["mem"],\
                              1,0,0)
        hostip=nfvdb.select_table(db,cursor,'t_host','ip',para['host_id'])
        hostpwd=nfvdb.select_table(db,cursor,'t_host','pwd',para['host_id'])
        remote_deploy.container_deploy(hostip,hostpwd,)
