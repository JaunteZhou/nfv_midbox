#!/usr/bin/python3
# -*- coding: utf-8 -*-
#del_function.py
import southbound.docker.remote_clear
import db.db_services
#para:
#{
#    "func_id":"<上层分配的功能id>"
#}
def del_function(para):
    db,cursor=db_services.connect_db()
    func_type=db_services.select_table(db,cursor,'t_function',para['func_id'])
    if func_type==():#空tuple：表示未查询到对应条目
        return[1,"Error:Function doesn't exist."]
    hostip=db_services.select_table(db,cursor,'t_host','ip',para['host_id'])
    if hostip==():
        return [1,"Error: Host doesn't exist."]
    hostpwd=db_services.select_table(db,cursor,'t_host','pwd',para['host_id'])
    
    if func_type==1:
        db_services.delete_table(db,cursor,'t_function',para["func_id"])
        remote_clear.container_clear(hostip,hostpwd,para['func_id'])
    elif func_type==2:#为虚拟机
        #TODO:此处删除虚拟机
        pass
    db_services.close_db(db,cursor)
    return[0,"Function Deleted Succesfully! "];