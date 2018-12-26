#!/usr/bin/python3
# -*- coding: utf-8 -*-
#image.py
import json

import rest_requests, CODE
from openstack_config import images_url


def getImagesList():
    """Show list of images."""
    code, res = rest_requests.get(images_url)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res["images"]

def getImage(image_id):
    """Show a image."""
    code, res = rest_requests.get(images_url + "/" + image_id)
    if code != CODE.OK_200:
        # TODO: log
        return None
    return res

def deleteImage(image_id):
    """Delete a Image."""
    code = rest_requests.delete(images_url + "/" + image_id)
    if code != CODE.NO_CONTENT_204:
        # TODO: log
        return False
    return True