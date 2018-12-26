#!/usr/bin/python3
# -*- coding: utf-8 -*-
#rest_requests.py
import json
import requests

from midbox.southbound.openstack.openstack_rest_api.identity import auth_token

headers = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "X-Auth-Token": auth_token
}

def get(url, payload=None):
    r = requests.get(url, headers=headers, params=payload)
    return r.status_code, r.json()

def post(url, body):
    r = requests.post(url, body, headers=headers)
    return r.status_code, r.json()

def put(url, body):
    r = requests.put(url, body, headers=headers)
    return r.status_code, r.json()

def delete(url):
    r = requests.delete(url, headers=headers)
    return r.status_code
