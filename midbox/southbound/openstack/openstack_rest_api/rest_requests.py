#!/usr/bin/python3
# -*- coding: utf-8 -*-
#rest_requests.py
import json
import requests

from midbox.southbound.openstack.openstack_rest_api.identity import AuthToken

at = AuthToken()

headers = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "X-Auth-Token": at.getToken()
}

def get(url, payload=None):
    headers["X-Auth-Token"] = at.getToken()
    r = requests.get(url, headers=headers, params=payload)
    return r.status_code, r.json()

def post(url, body):
    headers["X-Auth-Token"] = at.getToken()
    r = requests.post(url, body, headers=headers)
    if not r.text:
        print("Responed is None!")
        return r.status_code, {}
    return r.status_code, r.json()

def put(url, body):
    headers["X-Auth-Token"] = at.getToken()
    r = requests.put(url, body, headers=headers)
    return r.status_code, r.json()

def delete(url):
    headers["X-Auth-Token"] = at.getToken()
    r = requests.delete(url, headers=headers)
    return r.status_code, "End"
