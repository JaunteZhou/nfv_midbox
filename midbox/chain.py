#!/usr/bin/python
# -*- coding: utf-8 -*-
# chain.py
import logging

logger = logging.getLogger(__name__)

from midbox.southbound.ovs import ovs_services
from midbox.db import db_services
from midbox._config import TYPE_DOCKER, TYPE_OPENSTACK, IN_PORT, OUT_PORT
from midbox.southbound.openstack.openstack_services import getVmDataInAndOutPortsName


def setChain(para):
    """
    配置功能链接
    :param para: 包含以下四个元素的字典
                {
                    "func_ids": "xxxxxxxx-yyyyyyyy-zzzzzzzzz",
                    "match_field": "",
                    "priority": INT,
                    "chain_id": "xxxxxxxx"
                }
    :return: 二元组，包含一个指示执行结果的值（0成功，1失败）和字符串
    """
    # 必须初始化这两个端口名为有效的名称
    if IN_PORT == 'default' or OUT_PORT == 'default':
        logger.error("Physical Port Name has not been Initialized!")
        return 1, "Error: Physical Port Name has not been Initialized!"
    logger.debug('Start.')
    # 多个功能id
    func_ids = para["func_ids"]
    # 匹配域
    match_field = para["match_field"]
    # 流表优先级
    priority = para["priority"]
    # 链id
    chain_id = para["chain_id"]
    # 连接数据库
    db, cursor = db_services.connect_db()

    # 将字符串的功能id序列转换为列表，并且查找对应功能端口名
    ret_code, ret_data = __get_port_pair_list_of_func_list(db, cursor, func_ids)
    if ret_code == 1:
        return ret_code, ret_data
    func_id_list = ret_data[0]
    port_names_temp = ret_data[1]

    n = 0
    flag = 0
    # list结尾附一个0，使得循环达到最后一个功能时n+1不会溢出
    func_id_list.append('0')
    while 1:
        if n == len(func_id_list) - 1:
            aft = 0
            break
        __add_ref_count(db, cursor, func_id_list[n])
        bef = 0
        aft = 0
        if flag == 0:
            bef = 0
            flag = 1
        else:
            bef = func_id_list[n - 1]
        if __diff_host(db, cursor, func_id_list[n], func_id_list[n + 1]):
            aft = 0
            flag = 0
        else:
            aft = func_id_list[n + 1]

        ip, password = __get_host_ip_and_pwd_by_func_id(db, cursor, func_id_list[n])
        port_names = [port_names_temp[bef][0], port_names_temp[bef][1],
                      port_names_temp[func_id_list[n]][0], port_names_temp[func_id_list[n]][1],
                      port_names_temp[aft][0], port_names_temp[aft][1]]
        ovs_services.deployFlow(ip, password, port_names,
                                str(priority), match_field, IN_PORT, OUT_PORT)

        n = n + 1
    # end while
    db_services.insert_flow(db, cursor, chain_id, func_ids, match_field)
    db_services.close_db(db, cursor)
    return 0, "Success: Set Chain Successfully by OVS." + " Chain ID: " + str(chain_id)


def delChain(para):
    """
    删除功能链接
    :param para: 包含以下一个元素的字典
                {
                    "chain_id": "xxxxxxx"
                }
    :return: 二元组，包含一个指示执行结果的值（0成功，1失败）和字符串
    """
    logger.debug('Start.')
    # 必须初始化这两个端口名为有效的名称
    if IN_PORT == 'default' or OUT_PORT == 'default':
        return 1, "Error: Physical Port Name has not been Initialized"

    chain_id = para['chain_id']

    db, cursor = db_services.connect_db()
    func_ids = db_services.select_table(db, cursor, "t_flow", "chain", chain_id)
    if func_ids is None:
        return 1, "Error: Chain don't Exist!"

    # 将字符串的功能id序列转换为列表，并且查找对应功能端口名
    ret_code, ret_data = __get_port_pair_list_of_func_list(db, cursor, func_ids)
    if ret_code == 1:
        return ret_code, ret_data
    func_id_list = ret_data[0]
    port_names_temp = ret_data[1]

    match_field = db_services.select_table(db, cursor, "t_flow", "match_field", chain_id)
    n = 0
    flag = 0
    # list结尾附一个0，使得循环达到最后一个功能时n+1不会溢出
    func_id_list.append('0')
    while 1:
        if n == len(func_id_list) - 1:
            aft = 0
            break
        err = __dec_ref_count(db, cursor, func_id_list[n])
        if err < 0:
            logger.error("Over Deleted!")
            return 1, "Error: Over Deleted!"
        elif err == 1:
            shutdown_flag = 1
        else:
            shutdown_flag = 0
        bef = 0

        if flag == 0:
            bef = 0
            flag = 1
        else:
            bef = func_id_list[n - 1]
        if __diff_host(db, cursor, func_id_list[n], func_id_list[n + 1]):
            flag = 0

        ip, password = __get_host_ip_and_pwd_by_func_id(db, cursor, func_id_list[n])
        port_names = [port_names_temp[bef][0], port_names_temp[bef][1],
                      port_names_temp[func_id_list[n]][0], port_names_temp[func_id_list[n]][1]]
        ovs_services.undeployFlow(ip, password, port_names, str(shutdown_flag), match_field, IN_PORT)

        n = n + 1
    # end while
    db_services.delete_table(db, cursor, "t_flow", chain_id)
    db_services.close_db(db, cursor)
    return 0, "Success: Delete Chain Successfully by OVS."


def __check_valid(db, cursor, id_list):
    for id in id_list:
        if db_services.select_table(db, cursor, "t_function", "host_id", id) == "None":
            return False
    return True


def __add_ref_count(db, cursor, id):
    refcount = db_services.select_table(db, cursor, "t_function", "ref_count", id)
    db_services.update_table(db, cursor, "t_function", "ref_count", refcount + 1, id)
    return 0


def __diff_host(db, cursor, id1, id2):
    if db_services.select_table(db, cursor, "t_function", "host_id", id1) != \
            db_services.select_table(db, cursor, "t_function", "host_id", id2):
        return True
    else:
        return False


def __dec_ref_count(db, cursor, id):
    refcount = db_services.select_table(db, cursor, "t_function", "ref_count", id)
    if refcount < 0:
        return -1
    db_services.update_table(db, cursor, "t_function", "ref_count", refcount - 1, id)
    if refcount == 0:
        return 1
    return 0


def __get_port_pair_list_of_func_list(db, cursor, func_ids):
    func_id_list = func_ids.split('-')
    port_names_temp = {0: ("phy", "phy")}

    if not __check_valid(db, cursor, func_id_list):
        logger.error("Function(s) don't Exist!")
        return 1, "Error: Function(s) don't Exist!"

    for f_id in func_id_list:
        func_type = db_services.select_table(db, cursor, "t_function", "type", f_id)
        # 获得虚拟机端口名的方法
        if func_type == TYPE_DOCKER:
            port_names_temp[f_id] = ("br-c" + f_id + "-in", "br-c" + f_id + "-out")
        elif func_type == TYPE_OPENSTACK:
            func_local_id = db_services.select_table(db, cursor, "t_function", "func_local_id", f_id)
            port_names_temp[f_id] = getVmDataInAndOutPortsName(func_local_id)
        else:
            logger.error("Function don't have Correct Type!")
            return 1, "Error: Function don't have Correct Type!"
    return 0, (func_id_list, port_names_temp)


def __get_host_ip_and_pwd_by_func_id(db, cursor, func_id):
    host_id = db_services.select_table(db, cursor, "t_function", "host_id", func_id)
    ip = db_services.select_table(db, cursor, "t_host", "ip", host_id)
    password = db_services.select_table(db, cursor, "t_host", "pwd", host_id)
    return ip, password
