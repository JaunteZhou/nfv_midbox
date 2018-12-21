#!/usr/bin/python3
# -*- coding: utf-8 -*-
#volume.py
import json

from openstack_rest_api import rest_requests, CODE
from openstack_rest_api.openstack_config import volumes_url

def getVolumesList():
    """Get volumes list."""
    code, res = rest_requests.get(volumes_url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    vl = res["volumes"]
    for i in range(len(vl)):
        vl[i].pop("links")
    return vl

def getVolumesDetail(volume_id):
    """Get volumes list with details."""
    code, res = rest_requests.get(volumes_url + "detail/" + volume_id)
    if code != CODE.OK_200:
        # TODO: log
        return None
    vl = res["volume"]
    vl.pop("links")
    return vl

def getVolumesListDetails():
    """Get volumes list with details."""
    code, res = rest_requests.get(volumes_url + "detail")
    if code != CODE.OK_200:
        # TODO: log
        return None
    vl = res["volumes"]
    for i in range(len(vl)):
        vl[i].pop("links")
    return vl

def createVolume(vol_size):
    """Create Volume by requested size of disk."""
    para_dic = {
        "volume":{
            "size": vol_size
        }
    }
    para_json = json.dumps(para_dic)
    code, res = rest_requests.post(volumes_url, para_json)
    if code != CODE.ACCEPTED_202:
        # TODO: log
        return None
    vl = res["volume"]
    vl.pop("links")
    return vl

def deleteVolume(v_id):
    """Delete volume by id."""
    code = rest_requests.delete(volumes_url + "/" + v_id)
    if code != CODE.ACCEPTED_202:
        # TODO: log
        return False
    return True

if __name__ == '__main__':
    print(getVolumesListDetails())