#!/usr/bin/python
# -*- coding: utf-8 -*-
#test.py
import json
import requests

jsonContent=[
    # DeployFunction
    [
        {
            "item":"FUNCTION",
            "method":"POST",
            "json":{
                "func_type":"container","func_id":"1",
                "host_id":"1","image_id":"1",
                "func_ip":"10.2.7.230/24","func_pwd":"123456",
                "cpu":"20","ram":"128","disk":"0"
            }
        },
        {
            "item":"FUNCTION",
            "method":"POST",
            "json":{
                "func_type":"container","func_id":"2",
                "host_id":"1","image_id":"2",
                "func_ip":"10.2.7.231/24","func_pwd":"123456",
                "cpu":"20","ram":"128","disk":"0"
            }
        },
        {
            "item":"FUNCTION",
            "method":"POST",
            "json":{
                "func_type":"container","func_id":"3",
                "host_id":"2","image_id":"2",
                "func_ip":"10.2.7.232/24","func_pwd":"123456",
                "cpu":"20","ram":"128","disk":"0"
            }
        }
    ],
    # DeleteFunction
    [
        {
            "item":"FUNCTION",
            "method":"DELETE",
            "json":{"func_id":"2"}
        }
    ],
    # DeployChain
    # TODO
    [
        {
            "item":"CHAIN",
            "method":"POST",
            "json":{
                "func_ids": "xxxxxxxx-yyyyyyyy-zzzzzzzzz",
                "match_field": "",
                "priority": 10,
                "chain_id": "xxxxxxxx"
            }
        }
    ],
    # DeleteChain
    [
        {
            "item":"CHAIN",
            "method":"DELETE",
            "json":{"chain_id": "1"}
        }
    ],
    # ShowStatus
    [
        {
            "item":"STATUS",
            "method":"GET",
            "json":{"":""}
        }
    ]
]

headers = {
    "Content-type": "application/json",
    "Accept": "application/json"
}

url = 'http://127.0.0.1:5000/nfvcmd'

while True:
    print("List of Test Items :")
    print("0: EXIT")
    print("1: DeployFunction")
    print("2: DeleteFunction")
    print("3: DeployChain")
    print("4: DeleteChain")
    print("5: ShowStatus")
    test_num=input("Input number of test item :")
    test_num=int(test_num)

    if test_num == 0:
        break
    elif test_num > 5:
        print("Error Input !")
        continue
    test_num -= 1

    for dic_item in jsonContent[test_num]:
        body = json.dumps(dic_item)
        print(body)
        r = requests.post(url, body, headers=headers)
        print("Code: ", r.status_code)
        print("Res : ", r.json())

        