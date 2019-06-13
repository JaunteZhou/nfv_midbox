#!/usr/bin/python
# -*- coding: utf-8 -*-
# registry.py

import pexpect
import re

from midbox._config import DOCKER_REGISTRY_IP, DOCKER_REGISTRY_PORT, DOCKER_REGISTRY_WORK_DIRECTORY, \
    DOCKER_SERVICE_FILE_PATH, IN_PORT, OUT_PORT, MAN_PORT, DATA_PLANE_SW_NAME, CTRL_PLANE_SW_NAME
from midbox.db import db_services
from midbox.southbound.remote_ssh import *

import logging


def registry_start():
    logger = logging.getLogger(__name__)

    db, cursor = db_services.connect_db()
    host_id_list = db_services.select_id(db, cursor, 't_host')
    chains = db_services.select_id(db, cursor, 't_flow')
    flag = 0
    if chains == []:
        flag = 1
    for host_id in host_id_list:
        ip = db_services.select_table(db, cursor, "t_host", "ip", host_id)
        pwd = db_services.select_table(db, cursor, "t_host", "pwd", host_id)
        exitstatus, rdata = remote_ssh(ip, pwd,
                                       r"sed -i -e \'s/ExecStart=.*dockerd.*\\s-H/ExecStart=\\/usr\\/bin\\/dockerd --insecure-registry=" +
                                       DOCKER_REGISTRY_IP + r":" + DOCKER_REGISTRY_PORT + r" -H/\' " + DOCKER_SERVICE_FILE_PATH)
        exitstatus, rdata = remote_ssh(ip, pwd, r"systemctl daemon-reload && systemctl restart docker.service")
        logger.info("Registry config initial info:" + rdata)

        # 顺便做点初始化工作
        exitstatus, rdata = remote_ssh(ip, pwd, r"ovs-vsctl add-br " + DATA_PLANE_SW_NAME)
        exitstatus, rdata = remote_ssh(ip, pwd, r"ovs-vsctl add-port " + DATA_PLANE_SW_NAME + " " + IN_PORT)
        exitstatus, rdata = remote_ssh(ip, pwd, r" ovs-vsctl add-port " + DATA_PLANE_SW_NAME + " " + OUT_PORT)
        exitstatus, rdata = remote_ssh(ip, pwd, r"ovs-vsctl add-br " + CTRL_PLANE_SW_NAME)
        exitstatus, rdata = remote_ssh(ip, pwd, "ovs-vsctl add-port " + CTRL_PLANE_SW_NAME + " " + MAN_PORT)
        if flag == 1:
            exitstatus, rdata = remote_ssh(ip, pwd, "ovs-ofctl del-flows " + DATA_PLANE_SW_NAME)

    child = pexpect.spawn('docker run -d -p ' + DOCKER_REGISTRY_PORT + ':5000 --restart always -v ' +
                          DOCKER_REGISTRY_WORK_DIRECTORY + ':/var/lib/registry --name myrepo registry ')
    exit = child.exitstatus
    rdata = child.read().decode()
    logger.debug(rdata)
    if exit != 0:
        if re.findall('is already in use by container', rdata) != []:
            logger.debug('Registry container is always existing!')
            child.close(force=True)
            child = pexpect.spawn('docker start myrepo')
            logger.debug(child.read())
            if child.exitstatus != 0:
                return [1, 'Registry start error']
        else:
            return [1, 'Registry start error']
    child.close(force=True)
    db_services.close_db(db, cursor)
