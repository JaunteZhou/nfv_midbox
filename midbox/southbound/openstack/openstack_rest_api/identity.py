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
    return r.headers.get('X-Subject-Token'), r.json()["token"]["expires_at"]

auth_token, expires_at = getToken()
# expires_at = '2019-03-13T14:59:49.000000Z'
expires_str = expires_at.replace("T", " ").split(".")[0]
logger.debug(expires_str)
expires_dt = datetime.datetime.strptime(expires_str, "%Y-%m-%d %H:%M:%S")

logger.debug(auth_token)
logger.debug(datetime.datetime.now())
logger.debug( (datetime.datetime.now()-expires_dt).total_seconds() )

if __name__ == '__main__':
    print (auth_token)
