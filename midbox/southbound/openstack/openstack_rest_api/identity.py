#!/usr/bin/python3
# -*- coding: utf-8 -*-
# identity.py
import json
import requests
import logging
import datetime
logger = logging.getLogger(__name__)

from midbox._config import USER_ID, USER_PWD, PROJECT_ID, auth_token_url

THRESHOLD_TIME_FOR_UPDATE = 600


class AuthToken:
    def __init__(self):
        self.auth_token = ""
        self.json_para = self.composeAuthPara(USER_ID, USER_PWD, PROJECT_ID)
        self.expires_time = datetime.datetime.now()

    def composeAuthPara(self, user_id, password, proj_id):
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

    def getToken(self):
        if (self.expires_time - datetime.datetime.now()).total_seconds() < THRESHOLD_TIME_FOR_UPDATE:
            logger.debug('Start Get Token.')
            headers = {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
            r = requests.post(auth_token_url, self.json_para, headers=headers)
            if r.status_code != requests.codes.created:
                logger.error(r.status_code)
                return ""
            # expires_at = '2019-03-13T14:59:49.000000Z'
            expires_at = r.json()["token"]["expires_at"]
            expires_at_for_dt = expires_at.replace("T", " ").split(".")[0]
            self.expires_time = datetime.datetime.strptime(expires_at_for_dt, "%Y-%m-%d %H:%M:%S")
            self.auth_token = r.headers.get('X-Subject-Token')
        
        return self.auth_token


if __name__ == '__main__':
    pass
