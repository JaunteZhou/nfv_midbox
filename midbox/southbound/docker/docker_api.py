#!/usr/bin/python
# -*- coding: utf-8 -*-
# docker_api.py

import logging

logger = logging.getLogger(__name__)

from midbox.db import db_services
from midbox.southbound.docker import docker_services
from midbox._config import TYPE_DOCKER


def addFunc(para):
    # TODO: check id
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    # 从数据库中根据镜像id获取镜像名称
    image_name = db_services.select_table(db, cursor, 't_image', 'func', para['image_id'])
    # 在指定主机上创建容器
    ret = docker_services.addContainer(para["host_ip"], para["host_pwd"],
                                       para['cpu'], para['ram'], image_name,
                                       para['func_id'], para['func_ip'])
    if ret is None:
        logger.error("Set Container Function Failed by Docker!")
        return 1, "Error: Set Container Function Failed by Docker!"
    # 在数据库中写入记录
    db_services.insert_function(db, cursor, para["func_id"], para["image_id"],
                                para["host_id"], 0, para["func_ip"], para["func_pwd"],
                                para["cpu"], para["ram"], TYPE_DOCKER, 0, 0)

    db_services.close_db(db, cursor)
    return 0, "Success: Set Container Function Successfully by Docker."


def delFunc(para):
    logger.debug('Start.')
    db, cursor = db_services.connect_db()

    host_id = db_services.select_table(db, cursor, 't_function', 'host_id', para['func_id'])
    host_ip = db_services.select_table(db, cursor, 't_host', 'ip', host_id)
    if len(host_ip) == 0:
        logger.error("Delete container Failed because Host doesn't Exist by Docker!")
        return 1, "Error: Delete container Function Failed because Host doesn't Exist by Docker!"
    host_pwd = db_services.select_table(db, cursor, 't_host', 'pwd', host_id)

    docker_services.delContainer(host_ip, host_pwd, para['func_id'])
    db_services.delete_table(db, cursor, 't_function', para["func_id"])

    db_services.close_db(db, cursor)
    return 0, "Success: Delete Container Function Successfully by Docker."


def moveFunc(para):
    logger.debug('Start.')
    return 1, "Error: Move Container Function by Docker because method is not perpared!"