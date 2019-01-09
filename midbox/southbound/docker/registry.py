#!/usr/bin/python
# -*- coding: utf-8 -*-
#registry.py

import pexpect
import re
from midbox._config import DOCKER_REGISTRY_IP,DOCKER_REGISTRY_PORT,DOCKER_REGISTRY_WORK_DIRECTORY
import midbox.db.db_services
import logging

def registry_start():
    logger=logging.getLogger(__name__)
    child=pexpect.spawn('docker run -d -p '+DOCKER_REGISTRY_PORT+':5000 --restart always -v '+DOCKER_REGISTRY_WORK_DIRECTORY+':/var/lib/registry --name myrepo registry ')
    exit=child.exitstatus
    rdata=child.read().decode()
    logger.debug(rdata)
    if exit!=0:
        if re.findall('is already in use by container',rdata)!=[]:
            logger.debug('Registry container is always existing!')
            child.close(force = True)
            child=pexpect.spawn('docker start myrepo')
            logger.debug(child.read())
            if child.exitstatus!=0:
                return [1,'Registry start error'];
        else:
            return [1,'Registry start error'];
    chile.close(force=True)
