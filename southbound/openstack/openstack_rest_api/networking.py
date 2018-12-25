#!/usr/bin/python3
# -*- coding: utf-8 -*-
#networking.py
"""This module provides a series of openstack networkding APIs"""
import json

from openstack_rest_api import rest_requests, CODE
from openstack_rest_api.openstack_config import networks_url

def getNetworksDetails(network_id):
    """Get details of Networks."""
    code, res = rest_requests.get(networks_url + "/" + network_id)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["network"]

def getNetworksList():
    """Get list of Networks."""
    code, res = rest_requests.get(networks_url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["networks"]

def createNetwork(para_json):
    """Create a Network."""
    code, res = rest_requests.post(networks_url, para_json)
    if code != CODE.CREATED_201:
        # TODO: log
        print (res)
        return None
    return res["network"]

def updateNetwork(network_id, para_json):
    """Update a Network."""
    code, res = rest_requests.put(networks_url + "/" + network_id, para_json)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["network"]

def deleteNetwork(id):
    """Delete a Network."""
    code, res = rest_requests.delete(networks_url + "/" + id)
    if code != CODE.NO_CONTENT_204:
        # TODO: log
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