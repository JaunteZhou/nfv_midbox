#!/usr/bin/python
# -*- coding: utf-8 -*-
# function.py

import logging

logger = logging.getLogger(__name__)

from midbox.db import db_services
from midbox._config import TYPE_DOCKER, TYPE_OPENSTACK, STR_TYPE_TO_NUM_TYPE
from midbox.southbound.openstack import openstack_api
from midbox.southbound.docker import docker_api


PLATFORM_MAPPER = {
    TYPE_OPENSTACK: openstack_api,
    TYPE_DOCKER: docker_api
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

    para["host_ip"] = host_ip
    para["host_pwd"] = host_pwd
    func_type = STR_TYPE_TO_NUM_TYPE[para["func_type"]]
    ret_code, ret_data = PLATFORM_MAPPER[func_type].addFunc(para)

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

    host_id = db_services.select_table(db,cursor,'t_function','host_id', para['func_id'])
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

    para["host_ip"] = host_ip
    para["host_pwd"] = host_pwd

    ret_code, ret_data = PLATFORM_MAPPER[func_type].delFunc(para)

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

    # TODO:
    host_id = para['new_host_id']
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

    para["host_ip"] = host_ip
    para["host_pwd"] = host_pwd
    ret_code, ret_data = PLATFORM_MAPPER[func_type].moveFunc(para)

    db_services.close_db(db, cursor)
    return ret_code, ret_data
