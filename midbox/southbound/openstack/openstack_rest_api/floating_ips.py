#!/usr/bin/python3
# -*- coding: utf-8 -*-
#floating_ips.py
"""This module provides a series of openstack networkding APIs"""
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import floating_url

def getFloatingIpDetails(floatingip_id):
    """Get details of FloatingIp."""
    logger.debug('Start.')
    code, res = rest_requests.get(floating_url + "/" + floatingip_id)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["floatingip"]

def getFloatingIpsList():
    """Get list of FloatingIps."""
    logger.debug('Start.')
    code, res = rest_requests.get(floating_url)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["floatingips"]

def createFloatingIp(para_json):
    """Create a FloatingIp."""
    logger.debug('Start.')
    code, res = rest_requests.post(floating_url, para_json)
    if code != requests.codes.created:
        logger.error((str(code), res)
        return None
    return res["floatingip"]

def updateFloatingIp(id, para_json):
    """Update a FloatingIp."""
    logger.debug('Start.')
    code, res = rest_requests.put(floating_url + "/" + id, para_json)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["floatingip"]

def deleteFloatingIp(id):
    """Delete a FloatingIp."""
    logger.debug('Start.')
    code, res = rest_requests.delete(floating_url + "/" + id)
    if code != requests.codes.no_content:
        logger.error((str(code), res)
        return False
    return True


if __name__ == '__main__':
    print (getFloatingIpsList())