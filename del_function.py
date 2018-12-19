#!/usr/bin/python3
# -*- coding: utf-8 -*-
#del_function.py
import southbound.docker.remote_clear
import db.db_services
#para:
{
    "func_id":"<上层分配的功能id>"
}
def del_function(para):
    db,cursor=db_services.connect_db()
    func_type=db_services.select_table(db,cursor,'t_function',para['func_id'])
    if func_type==None:
        return[1,"Error:Function Doesn't exist."]
    if func_type==1:
        db_services.delete_table(db,cursor,'t_function',para["func_id"])
        hostip=db_services.select_table(db,cursor,'t_host','ip',para['host_id'])
        hostpwd=db_services.select_table(db,cursor,'t_host','pwd',para['host_id'])
        remote_clear.container_clear(hostip,hostpwd,para['func_id'])
    elif func_type==2:#为虚拟机
        #TODO:此处删除虚拟机
        pass
    db_services.close_db(db,cursor)
    return[0,"Function Deleted Succesfully! "];