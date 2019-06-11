#!/usr/bin/python
# -*- coding: utf-8 -*-
# openstack_api.py

import logging

logger = logging.getLogger(__name__)

from midbox.db import db_services
from midbox.southbound import remote_ssh
from midbox.southbound.openstack import openstack_services
from midbox._config import TYPE_OPENSTACK, OPENSTACK_SW_NAME, \
    DATA_PLANE_SW_NAME, CTRL_PLANE_SW_NAME


def __move_vm_ports(host_ip, host_pwd, para):
    # remote_ssh.remote_ssh(host_ip, host_pwd,
    #                       'ovs-vsctl add-br ' + DATA_PLANE_SW_NAME + ' && ' +
    #                       'ovs-vsctl add-br ' + CTRL_PLANE_SW_NAME)
    # 端口转移
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + OPENSTACK_SW_NAME + ' ' +
                          para['manPortName'] + ' && ' +
                          'ovs-vsctl add-port ' + CTRL_PLANE_SW_NAME + ' ' +
                          para['manPortName'])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + OPENSTACK_SW_NAME + ' ' +
                          para['dataPortsNameList'][0] + ' && ' +
                          'ovs-vsctl add-port ' + DATA_PLANE_SW_NAME + ' ' +
                          para['dataPortsNameList'][0])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + OPENSTACK_SW_NAME + ' ' +
                          para['dataPortsNameList'][1] + ' && ' +
                          'ovs-vsctl add-port ' + DATA_PLANE_SW_NAME + ' ' +
                          para['dataPortsNameList'][1])
    # 开启端口
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ifconfig ' + para['manPortName'] + ' up && ' +
                          'ifconfig ' + para['dataPortsNameList'][0] + ' up && ' +
                          'ifconfig ' + para['dataPortsNameList'][1] + ' up')
    return True


def __remove_vm_ports(host_ip, host_pwd, para):
    # remote_ssh.remote_ssh(host_ip, host_pwd,
    #                       'ovs-vsctl add-br ' + DATA_PLANE_SW_NAME + ' && ' +
    #                       'ovs-vsctl add-br ' + CTRL_PLANE_SW_NAME)
    # 端口转移
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + CTRL_PLANE_SW_NAME + ' ' +
                          para['manPortName'])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + DATA_PLANE_SW_NAME + ' ' +
                          para['dataPortsNameList'][0])
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ovs-vsctl del-port ' + DATA_PLANE_SW_NAME + ' ' +
                          para['dataPortsNameList'][1])
    # 删除端口
    remote_ssh.remote_ssh(host_ip, host_pwd,
                          'ip link del ' + para['manPortName'] + ' && ' +
                          'ip link del ' + para['dataPortsNameList'][0] + ' && ' +
                          'ip link del ' + para['dataPortsNameList'][1] + ' ')
    return True


def addFunc(para):
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    # 从数据库中根据镜像id获取镜像在openstack中的id
    image_local_id = db_services.select_table(db, cursor, 't_image',
                                              'image_local_id', para['image_id'])
    # 在指定主机上创建虚拟机
    ret = openstack_services.addVm(para['cpu'], para['ram'], para['disk'],
                                   image_local_id, para['host_id'])
    if ret is None:
        logger.error("Set VM Function Failed by OpenStack!")
        return 1, "Error: Set VM Function Failed by OpenStack!"

    __move_vm_ports(para["host_ip"], para["host_pwd"], ret)

    # 在数据库中写入记录
    db_services.insert_function(db, cursor, para["func_id"], para["image_id"],
                                para["host_id"], ret['serverId'],
                                para["func_ip"], para["func_pwd"], para["cpu"],
                                para["ram"], TYPE_OPENSTACK, para['disk'], 0)

    db_services.close_db(db, cursor)
    return 0, "Success: Set VM Function Successfully by OpenStack."


def delFunc(para):
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    # get func_local_id from t_func table
    func_local_id = db_services.select_table(db, cursor, 't_function',
                                             'func_local_id', para['func_id'])
    # delete vm by vm_id = func_local_id
    ret = openstack_services.delVm(func_local_id)
    if not ret:
        logger.error("Delete VM Function Failed by OpenStack!")
        return 1, "Error: Delete VM Function Failed by OpenStack!"

    __remove_vm_ports(para["host_ip"], para["host_pwd"], ret)

    db_services.delete_table(db, cursor, 't_function', para["func_id"])

    db_services.close_db(db, cursor)
    return 0, "Success: Delete VM Function Successfully by OpenStack."


def moveFunc(para):
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    # get func_local_id from t_func table
    func_local_id = db_services.select_table(db, cursor, 't_function',
                                             'func_local_id', para['func_id'])
    new_image_id = openstack_services.createServerInstanceImage(func_local_id)
    if new_image_id is None:
        logger.error("Move VM Function Failed by OpenStack!")
        return 1, "Error: Move VM Function Failed by OpenStack!"
    # 在指定主机上创建虚拟机
    ret = openstack_services.addVm(para['cpu'], para['ram'], para['disk'],
                                   new_image_id, para['new_host_id'])
    if ret is None:
        print("Error: Set VM Function Failed by OpenStack!")
        logger.error("Set VM Function Failed by OpenStack!")
        # return 1, "Error: Set VM Function Failed by OpenStack!"

    __move_vm_ports(para["host_ip"], para["host_pwd"], ret)

    # 更新数据库
    db_services.update_table(db, cursor, 't_function', 'func_local_id',
                             ret['serverId'], para['func_id'])

    # 删除旧虚拟机
    ret = openstack_services.delVm(func_local_id)
    if ret is False:
        print("Error: Delete VM Function Failed by OpenStack!")
        logger.error("Delete VM Function Failed by OpenStack!")
    ret = openstack_services.delImage(new_image_id)
    if ret is False:
        print("Error: Delete VM Image Failed by OpenStack!")
        logger.error("Delete VM Image Failed by OpenStack!")

    db_services.close_db(db, cursor)
    return 0, "Success: Move VM Function Successfully by OpenStack."
