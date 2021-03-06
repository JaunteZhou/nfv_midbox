#!/usr/bin/python
# -*- coding: utf-8 -*-
# showall.py
import logging

logger = logging.getLogger(__name__)

import re
import threading
from midbox.db import db_services

from midbox.southbound import remote_ssh
from midbox.southbound.openstack.openstack_rest_api.hypervisors import getHostsListDetails
from midbox.southbound.openstack.openstack_rest_api.servers import getServersListDetails

# 容器端口-流量映射字典，用于在线程执行函数与showContainerStatus之间传递端口流量值
port_traff = {}


def __get_traffic(ip, pwd, cid):
    ret_code, ret_data = remote_ssh.remote_ssh(ip, pwd, 'bash /gettraffic.sh br-c' + cid + '-out')
    global port_traff
    port_traff[str(cid)] = ret_data
    return ret_data


def showAllStatus(para):
    """
    获取所有状态信息
    :param para: 不会使用的参数，仅作为统一传参格式
    :return: 字典结构，如下
        {
            '<host_id>':{   # host_id来自于openstack管理计算节点所生成的id值
                'host':{

                }
                'docker':{
                    '<container_id>':{
                        'cpu': String,
                        'ram': String MB
                    },
                    '<container_id>':{...}
                }
                'openstack':{
                    '<vm_id>':{
                        'cpu': String,
                        'ram': String MB,
                        'disk': String GB
                    },
                    '<vm_id>':{...}
                }
            },
            '<host_id>':{...)
        }
    """
    logger.debug('Start.')

    res = {}

    db, cursor = db_services.connect_db()
    # host_id_list = db_services.select_id(db, cursor, 't_host')

    # get hosts info
    hosts_info_list = getHostsListDetails()

    for host_info in hosts_info_list:
        hid = host_info['id']
        hname = host_info['hypervisor_hostname']

        # get host info
        res[str(hid)] = {}
        res[str(hid)]['host'] = host_info

        # get vms info
        res[str(hid)]['openstack'] = show_vm_status(hname)

        # get containers info
        res[str(hid)]['docker'] = show_container_status(hid)

    # res_json = json.dumps(res)
    return 0, res


def show_container_status(host_id):
    logger.debug('Start.')

    db, cursor = db_services.connect_db()
    funcs_list = db_services.select_condition(db, cursor, 't_function', 'fe_id', 'host_id', host_id)
    ip = db_services.select_table(db, cursor, "t_host", "ip", host_id)
    pwd = db_services.select_table(db, cursor, "t_host", "pwd", host_id)

    # 启动多线程获得每个容器的对应端口流量
    # thread_list:dict
    thread_list = {}

    for id_iter in funcs_list:
        # 判断是否容器
        if db_services.select_table(db, cursor, 't_function', 'type', id_iter) == 1:
            t = threading.Thread(target=__get_traffic, args=(ip, pwd, str(id_iter),))
            thread_list[id_iter] = t
            t.start()

    # 由于remote_ssh的传参为字符串，shell执行时也识别字符串，故必须保证remote传过去的参数就含有反斜杠，保证shell解释时不会去掉引号
    exitstatus, rdata = remote_ssh.remote_ssh(
        ip, pwd, 'docker stats --format \\"table {{.Name}} {{.CPUPerc}} {{.MemUsage}}\\" --no-stream')

    # 由于容器名均以c开头，故pattern使用了c开头去掉第一行表头，以及可能会有的仓库容器
    pat = '^c.*$'
    # 获取全部行
    reg_result = re.findall(pat, rdata, re.M)

    lineno = 0
    # return_list = []
    res = {}
    exp = re.compile(r'c(\d*) (\d.*%) (\d.*?[MG]iB)')
    for row_iter in reg_result:
        # 从每行获取所需数据
        temp = exp.search(reg_result[lineno])
        # cid 取字符串
        cid = temp.group(1)
        # 必须保证对应线程已退出，成功获取了端口流量
        t = thread_list[int(cid)]
        t.join()

        needs_docker_info = {
            'cpu': temp.group(2),
            'ram': temp.group(3),
            'traffic': port_traff[cid]
        }
        # return_list.append([id,cpu,mem])
        res[cid] = needs_docker_info
        lineno = lineno + 1

    db_services.close_db(db, cursor)
    # return return_list
    return res


def show_vm_status(host_name):
    logger.debug('Start.')

    # get vms info
    all_vms_info = getServersListDetails()
    res = {}
    for vm_info in all_vms_info:
        if vm_info['OS-EXT-SRV-ATTR:host'] == host_name:
            flavor = vm_info['flavor']['id']
            # eq: flavor.id = F-1-256-1 means vcpus=1, ram=256MB, disk=1GB
            resources_info = flavor.split('-')
            if len(resources_info) < 4:
                continue
            needs_vm_info = {
                'cpu': resources_info[1],
                'ram': resources_info[2],
                'disk': resources_info[3],
                'status': vm_info['status']
            }
            res[vm_info['id']] = needs_vm_info
    return res


if __name__ == '__main__':
    showAllStatus(None)
