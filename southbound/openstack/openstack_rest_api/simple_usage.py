#!/usr/bin/python3
# -*- coding: utf-8 -*-
#simple_usage.py
"""This module provides a series of openstack compute APIs"""
import json

from openstack_rest_api import rest_requests
from openstack_rest_api.openstack_config import simple_usage_url

def getAllSimpleTenantUsage(detailed=0):
    """List Tenant Usage Statistics For All Tenants"""
    # code, res = rest_requests.get(simple_usage_url + "?detailed=" + str(detailed))
    payload = {"detailed": detailed}
    code, res = rest_requests.get(simple_usage_url, payload)
    if code != 200:
        # TODO: log
        return None
    return res

def getSimpleTenantUsage(id):
    """Get usage statistics of a tenant"""
    code, res = rest_requests.get(simple_usage_url + "/" + id)
    if code != 200:
        # TODO: log
        return None
    return res


if __name__ == '__main__':
    print (getAllSimpleTenantUsage())