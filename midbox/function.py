#!/usr/bin/python
# -*- coding: utf-8 -*-
#function.py

from midbox.southbound.docker import remote_deploy, remote_clear
from midbox.southbound.openstack import openstack_services
from midbox.southbound.openstack.openstack_para import composeServerInstanceDictPara
from midbox.db import db_services
from midbox.midbox_config import TYPE_DOCKER, TYPE_OPENSTACK

"""
para:
{
   "func_type":"<container/vm>",
   "func_id":"<上层分配的功能编号>",
   "host_id":"<上层指定的部署位置>",
   "image_id":"<功能使用的镜像id>",
   "func_ip":"<上层为功能实体分配的ip地址>",        # TODO：ip 地址由上层指定？
   "func_pwd":"<功能实体ssh登录密码，若为容器则应使用默认密码>",
   "cpu":"<功能使用的CPU情况，注意区分容器和虚拟机使用的不同单位>",
   "ram":"<功能内存限制>"
   "disk":"<功能硬盘容量限制，这个项目对容器是无效的>"
}
"""
def setFunction(para):
    logger.debug('Start.')

    db,cursor = db_services.connect_db()
    hostip = db_services.select_table(db,cursor,'t_host','ip',para['host_id'])
    if hostip == ():
        #空tuple表示未查询到对应条目
        return [1,"Error: Host doesn't exist."]
    hostpwd = db_services.select_table(db,cursor,'t_host','pwd',para['host_id'])
    
    if para["func_type"] == "container":
        # get image name by image id from db
        imagename = db_services.select_table(db, cursor,
                't_image', 'func', para['image_id'])
        # create container in specified host
        ret = remote_deploy.container_deploy(hostip, hostpwd, 
                para['cpu'], para['ram'], imagename,
                para['func_id'],para['func_ip'])
        if ret == None:
            return [1, "Error?"]
        # add a record to db
        db_services.insert_function(db, cursor, 
                para["func_id"], para["image_id"], para["host_id"],0,
                para["func_ip"], para["func_pwd"], para["cpu"], para["ram"],
                TYPE_DOCKER, 0, 0)        
    elif para["func_type"] == "vm":
        image_local_id = db_services.select_table(db, cursor, 't_image', 'image_local_id', para['image_id'])
        # get vm_id by host id, for specified host location
        same_host = openstack_services.getSameHostInstanceId(para['host_id'])
        # create vm in specified host
        vm_para = composeServerInstanceDictPara(para['cpu'], para['ram'], para['disk'], image_local_id, same_host)
        ret = openstack_services.addVm(vm_para)
        # TODO: 先确认是否新建，再修改数据库

        # add a record to db
        db_services.insert_function(db, cursor, 
                para["func_id"], para["image_id"], para["host_id"], ret['server_id'],
                para["func_ip"], para["func_pwd"], para["cpu"], para["ram"],
                TYPE_OPENSTACK, para['disk'], 0)
    db_services.close_db(db,cursor)
    return [0,"Function Created Succesfully! IP:"+para['func_ip']]


"""
para:
{
   "func_id":"<上层分配的功能id>"
}
"""
def delFunction(para):
    logger.debug('Start.')
    
    db,cursor = db_services.connect_db()
    func_type = db_services.select_table(db, cursor, 't_function', 'type', para['func_id'])     # 增加了‘type’这一参数，请检查是否正确
    hostid=db_services.select_table(db,cursor,'t_function','host_id',para['func_id'])
    if func_type == ():
            #空tuple：表示未查询到对应条目
            return[1,"Error:Function doesn't exist."]

    if func_type == TYPE_DOCKER:
        
        hostip = db_services.select_table(db, cursor, 't_host', 'ip', hostid)
        if hostip == ():
            return [1,"Error: Host doesn't exist."]
        hostpwd = db_services.select_table(db,cursor,'t_host','pwd',hostid)

        remote_clear.container_clear(hostip,hostpwd,para['func_id'])
        # TODO: 先确认是否删除，再修改数据库
        db_services.delete_table(db,cursor,'t_function',para["func_id"])
    elif func_type == TYPE_OPENSTACK:
        # TODO: 删除错误，或许func_local_id
        openstack_services.delVm(para['func_id'])
        # TODO: 先确认是否删除，再修改数据库
        db_services.delete_table(db,cursor,'t_function',para["func_id"])
        pass
    db_services.close_db(db,cursor)
    return [0,"Function Deleted Succesfully! "]