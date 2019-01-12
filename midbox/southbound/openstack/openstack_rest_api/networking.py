#!/usr/bin/python3
# -*- coding: utf-8 -*-
#networking.py
"""This module provides a series of openstack networkding APIs"""
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import networks_url

def getNetworksDetails(network_id):
    """Get details of Networks."""
    logger.debug('Start.')
    code, res = rest_requests.get(networks_url + "/" + network_id)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["network"]

def getNetworksList():
    """Get list of Networks."""
    logger.debug('Start.')
    code, res = rest_requests.get(networks_url)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["networks"]

def createNetwork(para_json):
    """Create a Network."""
    logger.debug('Start.')
    code, res = rest_requests.post(networks_url, para_json)
    if code != requests.codes.created:
        logger.error((str(code), res)
        print (res)
        return None
    return res["network"]

def updateNetwork(network_id, para_json):
    """Update a Network."""
    logger.debug('Start.')
    code, res = rest_requests.put(networks_url + "/" + network_id, para_json)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["network"]

def deleteNetwork(id):
    """Delete a Network."""
    logger.debug('Start.')
    code, res = rest_requests.delete(networks_url + "/" + id)
    if code != requests.codes.no_content:
        logger.error((str(code), res)
        return False
    return True

### Trunk networking
### Router
### Subnet
### Firewall '/fwaas'

if __name__ == '__main__':
    # n = Networking()
    # print(n.getNetworksList())

    # nets = getNetworksList()
    # print (li)
    # for n in nets:
    #     print (n)
    #     print (n["name"])
    #     if n["name"] == "net_ctrl_plane":
    #         print (n["id"])

    # json_para = composeNetworkPara(name="data_net")
    para = {
        "network": {
            "admin_state_up": True,
            "name": "net1",
            "provider:network_type": "flat",
            "provider:segmentation_id": 2
        }
    }
    json_para = json.dumps(para)
    print (createNetwork(json_para))