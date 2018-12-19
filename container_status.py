#!/usr/bin/python3
# -*- coding: utf-8 -*-
#containerStatus.py

from db import db_services
import re
from southbound.docker import remote_ssh

def showContainerStatus(hostid:'int'):
    db,cursor = db_services.connect_db()
    funcs_list = db_services.select_condition(db,cursor,'t_function','fe_id','host_id',hostid)
    ip = db_services.select_table(db,cursor,"t_host","ip",hostid)
    pwd = db_services.select_table(db,cursor,"t_host","pwd",hostid)
    
    #由于remote_ssh的传参为字符串，shell执行时也识别字符串，故必须保证remote传过去的参数就含有反斜杠，保证shell解释时不会去掉引号
    exitstatus,rdata = remote_ssh.remote_ssh(ip,pwd,'docker stats --format \\"table {{.Name}} {{.CPUPerc}} {{.MemUsage}}\\" --no-stream')
    #回传的数据为字节流，需要解码为通常字符串数据进行正则匹配
    rdata = str(rdata,encoding = 'utf-8')
    print(rdata)

    #由于容器名均以c开头，故pattern使用了c开头去掉第一行表头
    pat = '^c.*$'
    #获取全部行
    reg_result = re.findall(pat,rdata,re.M)
    
    lineno = 0
    return_list = []
    exp = re.compile(r'c(\d*) (\d.*%) (\d.*?[MG]iB)')
    for id_iter in funcs_list:
        #从每行获取所需数据
        temp = exp.search(reg_result[lineno])
        id = int(temp.group(1))
        cpu = temp.group(2)
        mem = temp.group(3)
        lineno = lineno+1
        return_list.append([id,cpu,mem])

    db_services.close_db(db,cursor)
    return return_list