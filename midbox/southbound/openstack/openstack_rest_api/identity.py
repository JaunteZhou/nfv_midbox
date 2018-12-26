#!/usr/bin/python3
# -*- coding: utf-8 -*-
#identity.py
import json
import requests
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import openstack_config

def composeAuthPara(user_id, password, proj_id):
    para = {
        "auth": {
            "scope": {
                "project": {
                    "id": proj_id
                }
            },
            "identity": {
                "password": {
                    "user": {
                        "password": password,
                        "id": user_id
                    }
                },
                "methods": [
                    "password"
                ]
            }
        }
    }
    return json.dumps(para)

def getToken():
    logger.debug('Start.')
    para_json = composeAuthPara(
            openstack_config.user_id, 
            openstack_config.password,
            openstack_config.tenant_id)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    r = requests.post(
            openstack_config.auth_token_url, 
            para_json, 
            headers=headers)
    if r.status_code != requests.codes.created:
        logger.error('HttpCode: ' + str(code) + ' - Res: ' + res + '.')
        return ""
    return r.headers.get('X-Subject-Token')

auth_token = getToken()


if __name__ == '__main__':
    print (auth_token)
