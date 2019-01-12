#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ports.py
"""This module provides a series of openstack networkding APIs"""
import sys
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import ports_url

def getPortsDetails(port_id):
    """Get list of Ports."""
    logger.debug('Start.')
    code, res = rest_requests.get(ports_url + "/" + port_id)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["port"]

def getPortsList():
    """Get list of Ports."""
    logger.debug('Start.')
    code, res = rest_requests.get(ports_url)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["ports"]

def createPort(para_json):
    """Create a Port."""
    logger.debug('Start.')
    code, res = rest_requests.post(ports_url, para_json)
    if code != requests.codes.created:
        logger.error((str(code), res)
        return None
    return res["port"]

def updatePort(port_id, para_json):
    """Update a Port."""
    logger.debug('Start.')
    code, res = rest_requests.put(ports_url + "/" + port_id, para_json)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["port"]

def deletePort(port_id):
    """Delete a Port."""
    logger.debug('Start.')
    code, res = rest_requests.delete(ports_url + "/" + port_id)
    if code != requests.codes.no_content:
        logger.error((str(code), res)
        return False
    return True