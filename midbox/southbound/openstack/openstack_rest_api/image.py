#!/usr/bin/python3
# -*- coding: utf-8 -*-
#image.py
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import images_url


def getImagesList():
    """Show list of images."""
    logger.debug('Start.')
    code, res = rest_requests.get(images_url)
    if code != requests.codes.ok:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return None
    return res["images"]

def getImage(image_id):
    """Show a image."""
    logger.debug('Start.')
    code, res = rest_requests.get(images_url + "/" + image_id)
    if code != requests.codes.ok:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return None
    return res

def deleteImage(image_id):
    """Delete a Image."""
    logger.debug('Start.')
    code, res = rest_requests.delete(images_url + "/" + image_id)
    if code != requests.codes.no_content:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return False
    return True