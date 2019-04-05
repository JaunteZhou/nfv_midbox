#!/usr/bin/python
# -*- coding: utf-8 -*-
# function.py
import logging

logger = logging.getLogger(__name__)

from midbox.southbound.docker import docker_services
from midbox.southbound import remote_ssh
from midbox.southbound.openstack import openstack_services
from midbox.db import db_services
from midbox._config import TYPE_DOCKER, TYPE_OPENSTACK


def __move_vm_ports(host_ip, host_pwd, para):
    # 端口转移
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port br-int ' + para['manPortName'] + ' && ' +
                          'ovs-vsctl add-port sw-man ' + para['manPortName'])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port br-int ' + para['dataPortsNameList'][0] + ' && ' +
                          'ovs-vsctl add-port sw1 ' + para['dataPortsNameList'][0])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port br-int ' + para['dataPortsNameList'][1] + ' && ' +
                          'ovs-vsctl add-port sw1 ' + para['dataPortsNameList'][1])
    # 开启端口
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ifconfig ' + para['manPortName'] + ' up && ' +
                          'ifconfig ' + para['dataPortsNameList'][0] + ' up && ' +
                          'ifconfig ' + para['dataPortsNameList'][1] + ' up')
    return True


def add_docker_func(db, cursor, para, host_ip, host_pwd):
    # TODO: check id
    # 从数据库中根据镜像id获取镜像名称
    image_name = db_services.select_table(db, cursor, 't_image', 'func', para['image_id'])
    # 在指定主机上创建容器
    ret = docker_services.addContainer(host_ip, host_pwd,
                                       para['cpu'], para['ram'], image_name,
                                       para['func_id'], para['func_ip'])
    if ret is None:
        logger.error("Set Container Function Failed by Docker!")
        return 1, "Error: Set Container Function Failed by Docker!"
    # 在数据库中写入记录
    db_services.insert_function(db, cursor,
                                para["func_id"], para["image_id"], para["host_id"], 0,
                                para["func_ip"], para["func_pwd"], para["cpu"], para["ram"],
                                TYPE_DOCKER, 0, 0)

    return 0, "Success: Set Container Function Successfully by Docker."


def del_docker_func(db, cursor, para):
    host_id = db_services.select_table(db, cursor,
                                       't_function', 'host_id', para['func_id'])
    host_ip = db_services.select_table(db, cursor, 't_host', 'ip', host_id)
    if len(host_ip) == 0:
        logger.error("Delete container Failed because Host doesn't Exist by Docker!")
        return 1, "Error: Delete container Function Failed because Host doesn't Exist by Docker!"
    host_pwd = db_services.select_table(db, cursor, 't_host', 'pwd', host_id)

    docker_services.delContainer(host_ip, host_pwd, para['func_id'])
    db_services.delete_table(db, cursor, 't_function', para["func_id"])

    return 0, "Success: Delete Container Function Successfully by Docker."


def add_openstack_func(db, cursor, para, host_ip, host_pwd):
    # 从数据库中根据镜像id获取镜像在openstack中的id
    image_local_id = db_services.select_table(db, cursor,
                                              't_image', 'image_local_id', para['image_id'])
    # 在指定主机上创建虚拟机
    ret = openstack_services.addVm(para['cpu'], para['ram'], para['disk'],
                                   image_local_id, para['host_id'])
    if ret is None:
        logger.error("Set VM Function Failed by OpenStack!")
        return 1, "Error: Set VM Function Failed by OpenStack!"

    __move_vm_ports(host_ip, host_pwd, ret)

    # 在数据库中写入记录
    db_services.insert_function(db, cursor,
                                para["func_id"], para["image_id"], para["host_id"], ret['serverId'],
                                para["func_ip"], para["func_pwd"], para["cpu"], para["ram"],
                                TYPE_OPENSTACK, para['disk'], 0)

    return 0, "Success: Set VM Function Successfully by OpenStack."


def del_openstack_func(db, cursor, para):
    # get func_local_id from t_func table
    func_local_id = db_services.select_table(db, cursor,
                                             't_function', 'func_local_id', para['func_id'])
    # delete vm by vm_id = func_local_id
    ret = openstack_services.delVm(func_local_id)
    if ret is False:
        logger.error("Delete VM Function Failed by OpenStack!")
        return 1, "Error: Delete VM Function Failed by OpenStack!"
    db_services.delete_table(db, cursor, 't_function', para["func_id"])
    return 0, "Success: Delete VM Function Successfully by OpenStack."


def move_openstack_func(db, cursor, para, host_ip, host_pwd):
    # get func_local_id from t_func table
    func_local_id = db_services.select_table(db, cursor,
                                             't_function', 'func_local_id', para['func_id'])
    new_image_id = openstack_services.createServerInstanceImage(func_local_id)
    if new_image_id is None:
        logger.error("Move VM Function Failed by OpenStack!")
        return 1, "Error: Move VM Function Failed by OpenStack!"
    # 在指定主机上创建虚拟机
    ret = openstack_services.addVm(para['cpu'], para['ram'], para['disk'],
                                   new_image_id, para['new_host_id'])
    if ret is None:
        logger.error("Set VM Function Failed by OpenStack!")
        return 1, "Error: Set VM Function Failed by OpenStack!"

    __move_vm_ports(host_ip, host_pwd, ret)

    # 更新数据库
    db_services.update_table(db, cursor, 't_function', 'func_local_id', ret['serverId'], para['func_id'])

    # 删除旧虚拟机
    ret = openstack_services.delVm(func_local_id)
    if ret is False:
        print("Delete VM Function Failed by OpenStack!")
        logger.error("Delete VM Function Failed by OpenStack!")
    ret = openstack_services.delImage(new_image_id)
    if ret is False:
        print("Delete VM Image Failed by OpenStack!")
        logger.error("Delete VM Image Failed by OpenStack!")
    return 0, "Success: Move VM Function Successfully by OpenStack."


MAP_PLATFORM_TO_FUNC = {
    "add": {
        "vm": add_openstack_func,
        "container": add_docker_func
    },
    "del": {
        TYPE_OPENSTACK: del_openstack_func,
        TYPE_DOCKER: del_docker_func
    },
    'move': {
        TYPE_OPENSTACK: move_openstack_func
    }
}


def setFunction(para):
    """
    增加功能实例
    :param para: 字典结构，如下
            {
                "func_type":"<虚拟化网络功能类型>",
                "func_id":"<分配的虚拟化网络功能编号>",
                "host_id":"<指定的虚拟化网络功能部署位置的物理计算节点编号>",
                "image_id":"<虚拟化网络功能使用的镜像编号>",
                "func_ip":"<为虚拟化网络功能实体分配的IP地址>",
                "func_mng":{
                    "func_user":"<虚拟化网络功能实体中设定的用于管理的用户名>",
                    "func_pwd":"<虚拟化网络功能实体管理用户登录的密码，若为容器则应使用默认密码>"
                },
                "func_config":{
                    "cpu":"<虚拟化网络功能所使用的CPU信息，不同的虚拟化平台对这一参数的单位定义有所不同，
                            例如OpenStack使用数量单位个，而Docker使用百分比>",
                    "ram":"<功能内存限制>"
                    "disk":"<功能硬盘容量限制，这个项目对容器是无效的>"
                },
                "other":{}
            }
    :return: 二元组，包含一个指示执行结果的值（0成功，1失败）和字符串
    """
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    host_ip = db_services.select_table(db, cursor, 't_host', 'ip', para['host_id'])
    if not host_ip:
        # host_ip为空，表示未查询到对应条目
        logger.error("Host's IP doesn't Exist!")
        return 1, "Error: Host's IP doesn't Exist!"
    host_pwd = db_services.select_table(db, cursor, 't_host', 'pwd', para['host_id'])
    if not host_pwd:
        # host_ip为空，表示未查询到对应条目
        logger.error("Host's Password doesn't Exist!")
        return 1, "Error: Host's Password doesn't Exist!"

    ret_code, ret_data = MAP_PLATFORM_TO_FUNC["add"][para["func_type"]](db, cursor, para, host_ip, host_pwd)

    db_services.close_db(db, cursor)
    return ret_code, ret_data + " IP:" + para['func_ip']


def delFunction(para):
    """
    删除功能实例
    :param para: 字典结构，如下
            {
               "func_id":"<上层分配的功能id>"
            }
    :return: 二元组，包含一个指示执行结果的值（0成功，1失败）和字符串
    """
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    func_type = db_services.select_table(db, cursor, 't_function', 'type', para['func_id'])
    if not func_type:
        # func_type为空，表示未查询到对应条目
        logger.error("Function doesn't Exist!")
        return 1, "Error: Function doesn't Exist!"

    ret_code, ret_data = MAP_PLATFORM_TO_FUNC["del"][func_type](db, cursor, para)

    db_services.close_db(db, cursor)
    return ret_code, ret_data


def moveFunction(para):
    logger.debug('Start.')
    db, cursor = db_services.connect_db()
    # TODO:
    func_type = db_services.select_table(db, cursor, 't_function', 'type', para['func_id'])
    if not func_type:
        # func_type为空，表示未查询到对应条目
        logger.error("Function doesn't Exist!")
        return 1, "Error: Function doesn't Exist!"

    host_id = db_services.select_table(db, cursor,
                                       't_function', 'host_id', para['func_id'])
    host_ip = db_services.select_table(db, cursor, 't_host', 'ip', host_id)
    if not host_ip:
        # host_ip为空，表示未查询到对应条目
        logger.error("Host's IP doesn't Exist!")
        return 1, "Error: Host's IP doesn't Exist!"
    host_pwd = db_services.select_table(db, cursor, 't_host', 'pwd', host_id)
    if not host_pwd:
        # host_ip为空，表示未查询到对应条目
        logger.error("Host's Password doesn't Exist!")
        return 1, "Error: Host's Password doesn't Exist!"

    ret_code, ret_data = MAP_PLATFORM_TO_FUNC["move"][func_type](db, cursor, para, host_ip, host_pwd)

    db_services.close_db(db, cursor)
    return ret_code, ret_data
