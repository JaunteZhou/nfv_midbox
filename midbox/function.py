#!/usr/bin/python
# -*- coding: utf-8 -*-
#function.py
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.docker import remote_deploy, remote_clear, remote_ssh
from midbox.southbound.openstack import openstack_services
from midbox.southbound.openstack.openstack_para import composeServerInstanceDictPara
from midbox.db import db_services
from midbox._config import TYPE_DOCKER, TYPE_OPENSTACK

"""
para:
{
    "vnf_type":"<虚拟化网络功能类型>",
    "vnf_id":"<分配的虚拟化网络功能编号>",
    "host_id":"<指定的虚拟化网络功能部署位置的物理计算节点编号>",
    "image_id":"<虚拟化网络功能使用的镜像编号>",
    "vnf_ip":"<为虚拟化网络功能实体分配的IP地址>",
    "vnf_mng":{
        "vnf_user":"<虚拟化网络功能实体中设定的用于管理的用户名>",
        "vnf_pwd":"<虚拟化网络功能实体管理用户登录的密码，若为容器则应使用默认密码>"
    },
    "vnf_config":{
        "cpu":"<虚拟化网络功能所使用的CPU信息，不同的虚拟化平台对这一参数的单位定义有所不同，例如OpenStack使用数量单位个，而Docker使用百分比>",
        "ram":"<功能内存限制>"
        "disk":"<功能硬盘容量限制，这个项目对容器是无效的>"
    },
    "other":{}
}
"""

MAP_PLATFORM_2_FUNC = {
    "add":{
        "openstack": addOpenStackFunc,
        "docker": addDockerFunc
    },
    "del":{
        TYPE_OPENSTACK: delOpenStackFunc,
        TYPE_DOCKER: delDockerFunc
    }
    
}
#TODO:添加上层参数的出错处理：如重复的func_id
def setFunction(para):
    logger.debug('Start.')
    db,cursor = db_services.connect_db()

    hostip = db_services.select_table(db,cursor,'t_host','ip',para['host_id'])
    if hostip == ():
        #空tuple表示未查询到对应条目
        return [1,"Error: Host doesn't exist."]
    hostpwd = db_services.select_table(db,cursor,'t_host','pwd',para['host_id'])

    MAP_PLATFORM_2_FUNC["add"][para["vnf_platform"]](db, cursor, para, hostip, hostpwd)

    db_services.close_db(db,cursor)
    return [0,"Function Created Succesfully! IP:"+para['func_ip']]

def addDockerFunc(db, cursor, para, hostip, hostpwd):
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
    return 0

def addOpenStackFunc(db, cursor, para, hostip, hostpwd):
    image_local_id = db_services.select_table(db, cursor, 
            't_image', 'image_local_id', para['image_id'])
    # create vm in specified host
    ret = openstack_services.addVm(para['cpu'], para['ram'], para['disk'], 
            image_local_id, para['host_id'])
    if ret == None:
        logger.error("Set VM Function")
        return [1,"Error: Set Function Failed."]
    # 端口转移
    remote_ssh.remote_ssh(hostip, hostpwd, 
            'ovs-vsctl del-port br-int ' + ret['manPortName'] + ' && ' \
            + 'ovs-vsctl add-port sw-man ' + ret['manPortName'])
    remote_ssh.remote_ssh(hostip, hostpwd, 
            'ovs-vsctl del-port br-int ' + ret['dataPortsNameList'][0] + ' && ' \
            + 'ovs-vsctl add-port sw1 ' + ret['dataPortsNameList'][0])
    remote_ssh.remote_ssh(hostip, hostpwd, 
            'ovs-vsctl del-port br-int ' + ret['dataPortsNameList'][1] + ' && ' \
            + 'ovs-vsctl add-port sw1 ' + ret['dataPortsNameList'][1])

    remote_ssh.remote_ssh(hostip, hostpwd,
            'ifconfig ' + ret['manPortName'] + ' up && ' \
            + 'ifconfig ' + ret['dataPortsNameList'][0] + ' up && ' \
            + 'ifconfig ' + ret['dataPortsNameList'][1] + ' up')
    # add a record to db
    db_services.insert_function(db, cursor, 
            para["func_id"], para["image_id"], para["host_id"], ret['serverId'],
            para["func_ip"], para["func_pwd"], para["cpu"], para["ram"],
            TYPE_OPENSTACK, para['disk'], 0)
    return 0

"""
para:
{
   "func_id":"<上层分配的功能id>"
}
"""
def delFunction(para):
    logger.debug('Start.')
    db,cursor = db_services.connect_db()

    # TODO: 增加了‘type’这一参数，请检查是否正确
    func_type = db_services.select_table(db, cursor, 't_function', 'type', para['func_id'])
    if func_type == ():
        #空tuple：表示未查询到对应条目
        return [1,"Error: Function doesn't exist."]

    MAP_PLATFORM_2_FUNC["del"][func_type](db, cursor, para)

    db_services.close_db(db,cursor)
    return [0,"Function Deleted Succesfully!"]

def delDockerFunc(db, cursor, para):
    hostid=db_services.select_table(db, cursor,
            't_function', 'host_id', para['func_id'])
    hostip = db_services.select_table(db, cursor, 't_host', 'ip', hostid)
    if len(hostip) == 0:
        return [1,"Error: Host doesn't exist."]
    hostpwd = db_services.select_table(db,cursor,'t_host','pwd',hostid)

    remote_clear.container_clear(hostip,hostpwd,para['func_id'])
    # TODO: 先确认是否删除，再修改数据库
    db_services.delete_table(db,cursor,'t_function',para["func_id"])
    return 0

def delOpenStackFunc(db, cursor, para):
    # get func_local_id from t_func table
    func_local_id = db_services.select_table(db, cursor, 
            't_function', 'func_local_id', para['func_id'])
    # delete vm by vm_id = func_local_id
    ret = openstack_services.delVm(func_local_id)
    if ret == False:
        logger.error("Delete Function")
        return [1,"Error: Function Deleted Faild."]
    db_services.delete_table(db,cursor,'t_function',para["func_id"])
    return 0