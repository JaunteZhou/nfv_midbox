#!/usr/bin/python3
# -*- coding: utf-8 -*-
#simple_usage.py
"""This module provides a series of openstack compute APIs"""
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import simple_usage_url

def getAllSimpleTenantUsage(detailed=0):
    """List Tenant Usage Statistics For All Tenants."""
    logger.debug('Start.')
    # code, res = rest_requests.get(simple_usage_url + "?detailed=" + str(detailed))
    payload = {"detailed": detailed}
    code, res = rest_requests.get(simple_usage_url, payload)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["tenant_usage"]

def getSimpleTenantUsage(tenant_id):
    """Get usage statistics of a tenant."""
    logger.debug('Start.')
    code, res = rest_requests.get(simple_usage_url + "/" + tenant_id)
    if code != requests.codes.ok:
        logger.error((str(code), res)
        return None
    return res["tenant_usage"]


if __name__ == '__main__':
    print (getAllSimpleTenantUsage())