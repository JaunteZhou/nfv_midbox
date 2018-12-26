#!/usr/bin/python3
# -*- coding: utf-8 -*-
#flavor.py
"""This module provides a series of openstack compute APIs"""
import json

from midbox.southbound.openstack.openstack_rest_api import rest_requests, CODE
from midbox.southbound.openstack.openstack_rest_api.openstack_config import flavor_url

def getFlavorsList():
    """Get list of flavors."""
    code, res = rest_requests.get(flavor_url)
    if code != CODE.OK_200:
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorsListDetails():
    """Get list of flavors with details."""
    code, res = rest_requests.get(flavor_url + "/detail")
    if code != CODE.OK_200:
        # TODO: log
        return code
    fl = res["flavors"]
    for i in range(len(fl)):
        fl[i].pop("links")
    return fl

def getFlavorDetail(flavor_id):
    """Get a flavor with detail."""
    code, res = rest_requests.get(flavor_url + "/" + flavor_id)
    if code != CODE.OK_200:
        # TODO: log
        return code
    return code, res

def createFlavor(para_json):
    # send post request
    code, res = rest_requests.post(flavor_url, para_json)
    if code != CODE.OK_200:
        # TODO: log
        return code
    return res["flavor"]

def deleteFlavor(flavor_id):
    """Delete a flavor by flavor_id."""
    code = rest_requests.delete(flavor_url + "/" + flavor_id)
    if code != CODE.ACCEPTED_202:
        # TODO: log
        return False
    return True
