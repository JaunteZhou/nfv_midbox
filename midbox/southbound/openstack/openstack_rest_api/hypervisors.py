#!/usr/bin/python3
# -*- coding: utf-8 -*-
#hypervisors.py
"""This module provides a series of openstack compute APIs"""
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox.southbound.openstack.openstack_rest_api.openstack_config import hypervisors_url

def getHostsList():
    """Get the list of hypervisors."""
    logger.debug('Start.')
    code, res = rest_requests.get(hypervisors_url)
    if code != requests.codes.ok:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return None
    return res["hypervisors"]
    # return res

def getHostsListDetails():
    """The function gets the state of hosts."""
    logger.debug('Start.')
    code, res = rest_requests.get(hypervisors_url + "/detail")
    if code != requests.codes.ok:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return None
    return res["hypervisors"]
    # return res

def getHostsStatistics():
    """The function gets the state of hosts."""
    logger.debug('Start.')
    url = hypervisors_url + "/statistics"
    code, res = rest_requests.get(url)
    if code != requests.codes.ok:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return None
    return res["hypervisor_statistics"]