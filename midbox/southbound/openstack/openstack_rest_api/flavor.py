#!/usr/bin/python3
# -*- coding: utf-8 -*-
#flavor.py
"""This module provides a series of openstack compute APIs"""
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import flavor_url

def getFlavorsList():
    """Get list of flavors."""
    logger.debug('Start.')
    code, res = rest_requests.get(flavor_url)
    if code != requests.codes.ok:
        logger.error((r.status_code, r.json()))
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorsListDetails():
    """Get list of flavors with details."""
    logger.debug('Start.')
    code, res = rest_requests.get(flavor_url + "/detail")
    if code != requests.codes.ok:
        logger.error((r.status_code, r.json()))
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorDetail(flavor_id):
    """Get a flavor with detail."""
    logger.debug('Start.')
    code, res = rest_requests.get(flavor_url + "/" + flavor_id)
    if code != requests.codes.ok:
        logger.error((r.status_code, r.json()))
        return code
    return code, res

def createFlavor(para_json):
    """Create a Flavor."""
    logger.debug('Start.')
    # send post request
    code, res = rest_requests.post(flavor_url, para_json)
    if code != requests.codes.ok:
        logger.error((r.status_code, r.json()))
        return code
    return res["flavor"]

def deleteFlavor(flavor_id):
    """Delete a flavor by flavor_id."""
    logger.debug('Start.')
    code, res = rest_requests.delete(flavor_url + "/" + flavor_id)
    if code != requests.codes.accepted:
        logger.error((r.status_code, r.json()))
        return False
    return True
