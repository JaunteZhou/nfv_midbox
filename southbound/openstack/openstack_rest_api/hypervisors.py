#!/usr/bin/python3
# -*- coding: utf-8 -*-
#hypervisors.py
"""This module provides a series of openstack compute APIs"""
import json

from openstack_rest_api import rest_requests
from openstack_rest_api.openstack_config import compute_url

hypervisors_url = compute_url + "/os-hypervisors"

def getHostsList():
    """Get the list of hypervisors."""
    code, res = rest_requests.get(hypervisors_url)
    if code != 200:
        # TODO: log
        return None
    return res["hypervisors"]

def getHostsListDetails():
    """The function gets the state of hosts."""
    url = hypervisors_url + "/detail"
    code, res = rest_requests.get(url)
    if code != 200:
        # TODO: log
        return None
    hosts = []
    for hypervisor in res["hypervisors"]:
        host = {
            "name": "nova:"+hypervisor["hypervisor_hostname"],
            "cpu": hypervisor["vcpus"] - hypervisor["vcpus_used"],
            "memory": hypervisor["free_ram_mb"],
            "disk": hypervisor["free_disk_gb"]
        }
        hosts.append(host)
    return hosts


if __name__ == '__main__':
    print (getHostsList())