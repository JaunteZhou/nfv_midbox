"""This module provides a series of openstack compute APIs"""
import sys
sys.path.append(r"/Users/JaunteZhou/Documents/NFV30py/nfv30py")
import json

import rest_requests
from openstack_config import flavor_url

def getFlavorsList():
    """Get list of flavors."""
    code, res = rest_requests.get(flavor_url)
    if code != 200:
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorsListDetails():
    """Get list of flavors with details."""
    code, res = rest_requests.get(flavor_url + "/detail")
    if code != 200:
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorDetail(id):
    """Get a flavor with detail."""
    code, res = rest_requests.get(flavor_url + "/" + id)
    return code, res

def createFlavor(para_json):
    # send post request
    code, res = rest_requests.post(flavor_url, para_json)
    return code, res

def deleteFlavor(id):
    """Delete a flavor by id."""
    code = rest_requests.delete(flavor_url + "/" + id)
    if code != 202:
        # TODO: log
        return False
    return True

def clearFlavors():
    """Clear a flavor."""
    fl = getFlavorsList()
    for i in range(len(fl)):
        code = deleteFlavor(fl[i]["id"])
        if code != 200:
            # TODO: log
            continue
    return True
