#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ports.py
"""This module provides a series of openstack networkding APIs"""
import sys
import json

from openstack_rest_api import rest_requests
from openstack_rest_api.openstack_config import ports_url

def getPortsList():
    """Get list of Ports."""
    code, res = rest_requests.get(ports_url)
    if code != 200:
        # TODO: log
        return None
    return res["ports"]

def createPort(para_json):
    """Create a Port."""
    code, res = rest_requests.post(ports_url, para_json)
    if code != 201:
        # TODO: log
        return None
    return res["port"]

def updatePort(id, para_json):
    """Update a Port."""
    code, res = rest_requests.put(ports_url + "/" + id, para_json)
    if code != 200:
        # TODO: log
        return None
    return res["network"]

def deletePort(id):
    """Delete a Port."""
    code = rest_requests.get(ports_url + "/" + id)
    if code != 204:
        # TODO: log
        return False
    return True


# if __name__ == '__main__':
    # import networking
    # sys.path.append(r"/Users/JaunteZhou/Documents/NFV30PY/nfv30py/southbound/ostk/")
    # import ostk_para, ostk_ctrler
    # json_para = ostk_para.composePortPara(name="prog_port_2_2", network_id=ostk_ctrler.getNetworkIdByName("net_ctrl_plane"))
    # print (createPort(json_para))