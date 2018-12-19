#!/usr/bin/python3
# -*- coding: utf-8 -*-
#floating_ips.py
"""This module provides a series of openstack networkding APIs"""
import json

from openstack_rest_api import rest_requests
from openstack_rest_api.openstack_config import floating_url

def getFloatingIpsList():
    """Get list of FloatingIps."""
    code, res = rest_requests.get(floating_url)
    if code != 200:
        # TODO: log
        return None
    return res["floatingips"]

def createFloatingIp(para_json):
    """Create a FloatingIp."""
    code, res = rest_requests.post(floating_url, para_json)
    if code != 201:
        # TODO: log
        print (res)
        return None
    return res["floatingip"]

def updateFloatingIp(id, para_json):
    """Update a FloatingIp."""
    code, res = rest_requests.put(floating_url + "/" + id, para_json)
    if code != 200:
        # TODO: log
        return None
    return res["floatingip"]

def deleteFloatingIp(id):
    """Delete a FloatingIp."""
    code, res = rest_requests.get(floating_url + "/" + id)
    if code != 204:
        # TODO: log
        return False
    return True


if __name__ == '__main__':
    print (getFloatingIpsList())