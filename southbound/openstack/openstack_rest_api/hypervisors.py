#!/usr/bin/python3
# -*- coding: utf-8 -*-
#hypervisors.py
"""This module provides a series of openstack compute APIs"""
import json

from openstack_rest_api import rest_requests, CODE
from openstack_rest_api.openstack_config import hypervisors_url


def getHostsList():
    """Get the list of hypervisors."""
    code, res = rest_requests.get(hypervisors_url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["hypervisors"]

def getHostsListDetails():
    """The function gets the state of hosts."""
    code, res = rest_requests.get(hypervisors_url + "/detail")
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["hypervisors"]

def getHostsStatistics():
    """The function gets the state of hosts."""
    url = hypervisors_url + "/statistics"
    code, res = rest_requests.get(url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["hypervisor_statistics"]