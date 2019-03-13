#!/usr/bin/python3
# -*- coding: utf-8 -*-
#identity.py
import json
import requests
import logging
import datetime
logger = logging.getLogger(__name__)

from midbox._config import user_id, password, tenant_id, auth_token_url

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
    para_json = composeAuthPara(user_id, password, tenant_id)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    r = requests.post(auth_token_url, para_json, headers=headers)
    if r.status_code != requests.codes.created:
        logger.error((r.status_code, r.json()))
        return ""
    return r.headers.get('X-Subject-Token'), r.json()["expires_at"]

auth_token, expires_at = getToken()
logger.debug(expires_at)
logger.debug(auth_token)
logger.debug(datetime.datetime.now())

if __name__ == '__main__':
    print (auth_token)
