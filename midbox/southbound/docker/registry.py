#!/usr/bin/python
# -*- coding: utf-8 -*-
#registry.py

import pexpect
import re
from midbox._config import DOCKER_REGISTRY_IP,DOCKER_REGISTRY_PORT,DOCKER_REGISTRY_WORK_DIRECTORY
import midbox.db.db_services

def registry_start():
    child=pexpect.spawn('docker run -d -p 5000:5000 --restart always -v '+DOCKER_REGISTRY_WORK_DIRECTORY+':/var/lib/registry --name myrepo registry ')
    exit=child.exitstatus
    rdata=child.read().decode()
    if exit!=0:
        if re.findall('is already in use by container',rdata)!=[]:
            child.close(force = True)
            child=pexpect.spawn('docker start myrepo')
            if child.exitstatus!=0:
                return [1,'Registry start error'];
        else:
            return [1,'Registry start error'];
    chile.close(force=True)
