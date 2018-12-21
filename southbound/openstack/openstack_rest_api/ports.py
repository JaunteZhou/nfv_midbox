#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ports.py
"""This module provides a series of openstack networkding APIs"""
import sys
import json

from openstack_rest_api import rest_requests, CODE
from openstack_rest_api.openstack_config import ports_url

def getPortsDetails(port_id):
    """Get list of Ports."""
    code, res = rest_requests.get(ports_url + "/" + port_id)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["port"]

def getPortsList():
    """Get list of Ports."""
    code, res = rest_requests.get(ports_url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["ports"]

def createPort(para_json):
    """Create a Port."""
    code, res = rest_requests.post(ports_url, para_json)
    if code != CODE.CREATED_201:
        # TODO: log
        return None
    return res["port"]

def updatePort(port_id, para_json):
    """Update a Port."""
    code, res = rest_requests.put(ports_url + "/" + port_id, para_json)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["port"]

def deletePort(port_id):
    """Delete a Port."""
    code = rest_requests.delete(ports_url + "/" + port_id)
    if code != CODE.NO_CONTENT_204:
        # TODO: log
        return False
    return True