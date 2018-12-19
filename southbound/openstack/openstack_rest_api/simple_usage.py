"""This module provides a series of openstack compute APIs"""
import sys
sys.path.append(r"/Users/JaunteZhou/Documents/NFV30py/nfv30py")
import json

import rest_requests
from openstack_config import simple_usage_url

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