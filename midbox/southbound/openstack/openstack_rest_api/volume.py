#!/usr/bin/python3
# -*- coding: utf-8 -*-
#volume.py
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import volumes_url

def getVolumesList():
    """Get volumes list."""
    logger.debug('Start.')
    code, res = rest_requests.get(volumes_url)
    if code != requests.codes.ok:
        logger.error((code, res))
        return None
    vl = res["volumes"]
    for i in range(len(vl)):
        vl[i].pop("links")
    return vl

def getVolumesDetail(volume_id):
    """Get volumes list with details."""
    logger.debug('Start.')
    code, res = rest_requests.get(volumes_url + "detail/" + volume_id)
    if code != requests.codes.ok:
        logger.error((code, res))
        return None
    vl = res["volume"]
    vl.pop("links")
    return vl

def getVolumesListDetails():
    """Get volumes list with details."""
    logger.debug('Start.')
    code, res = rest_requests.get(volumes_url + "detail")
    if code != requests.codes.ok:
        logger.error((code, res))
        return None
    vl = res["volumes"]
    for i in range(len(vl)):
        vl[i].pop("links")
    return vl

def createVolume(vol_size):
    """Create Volume by requested size of disk."""
    logger.debug('Start.')
    para_dic = {
        "volume":{
            "size": vol_size
        }
    }
    para_json = json.dumps(para_dic)
    code, res = rest_requests.post(volumes_url, para_json)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return None
    vl = res["volume"]
    vl.pop("links")
    return vl

def deleteVolume(v_id):
    """Delete volume by id."""
    logger.debug('Start.')
    code, res = rest_requests.delete(volumes_url + "/" + v_id)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return False
    return True

if __name__ == '__main__':
    print(getVolumesListDetails())