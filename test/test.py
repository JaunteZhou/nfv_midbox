#!/usr/bin/python
# -*- coding: utf-8 -*-
#showall.py

import pexpect

jsonContent={'DeployFunction':
             ['{"method":"POST","item":"FUNCTION","json":{"func_type":"container","func_id":"1","host_id":"1","image_id":"1","func_ip":"10.2.7.230/24","func_pwd":"123456","cpu":"20","mem":"128","disk":"0"}}',
              '{"method":"POST","item":"FUNCTION","json":{"func_type":"container","func_id":"2","host_id":"1","image_id":"2","func_ip":"10.2.7.231/24","func_pwd":"123456","cpu":"20","mem":"128","disk":"0"}}',
              '{"method":"POST","item":"FUNCTION","json":{"func_type":"container","func_id":"3","host_id":"2","image_id":"3","func_ip":"10.2.7.232/24","func_pwd":"123456","cpu":"20","mem":"128","disk":"0"}}',

             ],
             'DeleteFunction':
             ['{"method":"DELETE","item":"FUNCTION","json":{"func_id":"2"}}',

             ],
             'DeployChain':
             ['{"method":}'
             ]
            }

while True:
    testItem=input("Input the test item(DeployFunction/DeleteFunction/DeployChain/DeleteChain/ShowStatus/0 for exit):")
    if testItem=='0':
        break
    commonPrefix='curl http://127.0.0.1:5000/nfvcmd  -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '
    for item in jsonContent[testItem]:
        cmd='\''+item+'\''
        child=pexpect.spawn(commonPrefix+cmd)
        print(child.read())
        child.close()

        