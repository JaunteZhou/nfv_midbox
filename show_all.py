#!/usr/bin/python3
# -*- coding: utf-8 -*-
#showall.py

import json
from db import db_services
import container_status

#return a jsonified file including all NFs status;0 refers to successful execution.
def showall():
    res = {'containers':None,'VMs':None}
    db, cursor = db_services.connect_db()
    host_id_list = db_services.select_id(db, cursor, 't_host')
    
    for hid in host_id_list:
        containers = container_status.showContainerStatus(hid)
        for centry in containers:
            cid = centry[0]
            # TODO: res在什么地方修改了吗？None是不能取属性值的
            res['containers'][str[hid]][str[cid]][{'cpu':centry[1],'mem':centry[2]}]
    
    #此处获得全部虚拟机信息
    
    res_json = json.dumps(res)
    return [0,res_json]


if __name__=='__main__':
    showall()

