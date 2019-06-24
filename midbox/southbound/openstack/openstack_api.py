#!/usr/bin/python
# -*- coding: utf-8 -*-
# openstack_api.py

import logging

logger = logging.getLogger(__name__)

from midbox.db import db_services
from midbox.southbound.remote_ssh import remote_ssh
from midbox.southbound.openstack import openstack_services
from midbox._config import TYPE_OPENSTACK, OPENSTACK_SW_NAME, DATA_PLANE_SW_NAME, CTRL_PLANE_SW_NAME, \
    OPENSTACK_BR_NAME_HEAD, OPENSTACK_VETH_NAME_HEAD


def __get_br_name_of_port(port_name):
    return OPENSTACK_BR_NAME_HEAD + port_name[3:]


def __get_veth_name_of_port(port_name):
    return OPENSTACK_VETH_NAME_HEAD + port_name[3:]


def __move_vm_ports(host_ip, host_pwd, para):
    logger.debug('Start.')
    # remote_ssh(host_ip, host_pwd,
    #                       'ovs-vsctl add-br ' + DATA_PLANE_SW_NAME + ' && ' +
    #                       'ovs-vsctl add-br ' + CTRL_PLANE_SW_NAME)
    # 端口转移
    mng_port_name = para['manPortName']
    br_name_of_man_port = __get_br_name_of_port(mng_port_name)
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'brctl delif ' + br_name_of_man_port + ' ' + mng_port_name + ' && ' +
                                   'ovs-vsctl add-port ' + CTRL_PLANE_SW_NAME + ' ' + mng_port_name)
    logger.info(rdata)

    in_port_name = para['dataPortsNameList'][0]
    br_name_of_in_port = __get_br_name_of_port(in_port_name)
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'brctl delif ' + br_name_of_in_port + ' ' + in_port_name + ' && ' +
                                   'ovs-vsctl add-port ' + DATA_PLANE_SW_NAME + ' ' + in_port_name)
    logger.info(rdata)

    out_port_name = para['dataPortsNameList'][1]
    br_name_of_out_port = __get_br_name_of_port(out_port_name)
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'brctl delif ' + br_name_of_out_port + ' ' + out_port_name + ' && ' +
                                   'ovs-vsctl add-port ' + DATA_PLANE_SW_NAME + ' ' + out_port_name)
    logger.info(rdata)
    # 开启端口
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'ifconfig ' + mng_port_name + ' up && ' +
                                   'ifconfig ' + in_port_name + ' up && ' +
                                   'ifconfig ' + out_port_name + ' up')
    logger.info(rdata)
    return True


def __remove_vm_ports(host_ip, host_pwd, para):
    logger.debug('Start.')
    # remote_ssh(host_ip, host_pwd,
    #                       'ovs-vsctl add-br ' + DATA_PLANE_SW_NAME + ' && ' +
    #                       'ovs-vsctl add-br ' + CTRL_PLANE_SW_NAME)
    # 端口转移
    mng_port_name = para['manPortName']
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'ovs-vsctl del-port ' + CTRL_PLANE_SW_NAME + ' ' + mng_port_name)
    logger.info(rdata)

    in_port_name = para['dataPortsNameList'][0]
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'ovs-vsctl del-port ' + DATA_PLANE_SW_NAME + ' ' + in_port_name)
    logger.info(rdata)

    out_port_name = para['dataPortsNameList'][1]
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'ovs-vsctl del-port ' + DATA_PLANE_SW_NAME + ' ' + out_port_name)
    logger.info(rdata)
    # 删除端口
    mng_veth_port_name = __get_veth_name_of_port(mng_port_name)
    in_veth_port_name = __get_veth_name_of_port(in_port_name)
    out_veth_port_name = __get_veth_name_of_port(out_port_name)
    exitstatus, rdata = remote_ssh(host_ip, host_pwd,
                                   'ip link del ' + mng_veth_port_name + ' && ' +
                                   'ip link del ' + in_veth_port_name + ' && ' +
                                   'ip link del ' + out_veth_port_name + ' ')
    logger.info(rdata)
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

    # get old_func_local_id from t_func table
    old_func_local_id = db_services.select_table(db, cursor, 't_function',
                                             'func_local_id', para['func_id'])
    new_image_id = openstack_services.createServerInstanceImage(old_func_local_id)
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

    __move_vm_ports(para["new_host_ip"], para["new_host_pwd"], ret)

    # 更新数据库
    db_services.update_table(db, cursor, 't_function', 'func_local_id',
                             ret['serverId'], para['func_id'])

    # 删除旧虚拟机
    ret = openstack_services.delVm(old_func_local_id)
    if ret is False:
        print("Error: Delete VM Function Failed by OpenStack!")
        logger.error("Delete VM Function Failed by OpenStack!")

    __remove_vm_ports(para["old_host_ip"], para["old_host_pwd"], ret)

    ret = openstack_services.delImage(new_image_id)
    if ret is False:
        print("Error: Delete VM Image Failed by OpenStack!")
        logger.error("Delete VM Image Failed by OpenStack!")

    db_services.close_db(db, cursor)
    return 0, "Success: Move VM Function Successfully by OpenStack."
