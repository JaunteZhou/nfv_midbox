#!/usr/bin/python
# -*- coding: utf-8 -*-
# ovs_services.py

import logging

logger = logging.getLogger(__name__)

from midbox.southbound.remote_ssh import remote_ssh
from midbox._config import DATA_PLANE_SW_NAME


def deployFlow(ip, password, port_names,
               priority='1', match_field="",
               phy_in="ens7", phy_out="ens8"):
    """
    下发部署流表
    :param ip: 物理机ip地址
    :param password: 物理机密码
    :param port_names: 包含三个服务功能主体的共六个网卡名
                       若有物理网卡则出入口名称相同均为“phy”
    :param priority: 优先级
    :param match_field: 流匹配域（不含in_port）
    :param phy_in: 物理机流量入口名
    :param phy_out: 物理机流量出口名
    :return:
    """
    logger.debug('Start.')
    logger.info((port_names[0], port_names[4]))

    if port_names[0] != "phy":
        ft_item = __edit_flow_table_item(port_names[1], match_field, priority, "output:" + port_names[2])
    else:
        ft_item = __edit_flow_table_item(phy_in, match_field, priority, "output:" + port_names[2])
    ret_code, ret_data = __add_flow_to_ovs(ip, password, DATA_PLANE_SW_NAME, ft_item)
    logger.info(ret_data)

    if port_names[4] == "phy":
        ft_item = __edit_flow_table_item(port_names[3], match_field, priority, "output:" + phy_out)
    else:
        ft_item = __edit_flow_table_item(port_names[3], match_field, priority, "output:" + port_names[4])
    ret_code, ret_data = __add_flow_to_ovs(ip, password, DATA_PLANE_SW_NAME, ft_item)
    logger.info(ret_data)

    # 不再需要drop，只需保证OVS无NORMAL流表项即可，注释此行，确定无误后删除
    # ret_code,ret_data=remote_ssh(ip,password,
    # 'ovs-ofctl add-flow sw1 in_port='+port_names[2]+',actions=drop && ifconfig '+port_names[2]+' up')

    # 开启端口
    ret_code, ret_data = remote_ssh(ip, password, 'ifconfig ' + port_names[2] + ' up')
    logger.info(ret_data)

    return 0


def undeployFlow(ip, password, port_names, shutdown_flag, match_field="", phy_in="ens7"):
    """

    :param ip: 物理机ip地址
    :param password: 物理机密码
    :param port_names: 包含两个功能共四个网卡名，若有物理网卡则出入口名称相同均为“phy_in/phy_out”
    :param shutdown_flag: 指示当前容器是否没有被任何功能链使用，将由容器类的引用计数判断
    :param match_field: 流匹配域
    :param phy_in: 物理机流量入口名
    :return:
    """
    logger.debug('Start.')

    if shutdown_flag == "1":
        pass
        # ret_code, ret_data = remote_ssh(ip, password, 'ifconfig ' + port_names[2] + ' down')
        # logger.info(ret_data)

    if port_names[0] != "phy":
        ft_item = __edit_flow_table_item(port_names[1], match_field)
    else:
        ft_item = __edit_flow_table_item(phy_in, match_field)
    ret_code, ret_data = __del_ovs_flow(ip, password, DATA_PLANE_SW_NAME, ft_item)
    logger.info(ret_data)

    ft_item = __edit_flow_table_item(port_names[3], match_field)
    ret_code, ret_data = __del_ovs_flow(ip, password, DATA_PLANE_SW_NAME, ft_item)
    logger.info(ret_data)

    return 0


def __edit_flow_table_item(in_port, match_field='', priority='', actions=''):
    item = ''
    if priority:
        item = item + 'priority=' + priority + ','
    item = item + 'in_port=' + in_port
    if match_field:
        item = item + ',' + match_field
    if actions:
        item = item + ',actions=' + actions
    return item


def __add_flow_to_ovs(ip, password, sw, ft_item):
    cmd = 'ovs-ofctl add-flow ' + sw + ' ' + ft_item
    ret_code, ret_data = remote_ssh(ip, password, cmd)
    logger.info(ret_data)
    return ret_code, ret_data


def __del_ovs_flow(ip, password, sw, ft_item):
    cmd = 'ovs-ofctl del-flows ' + sw + ' ' + ft_item
    ret_code, ret_data = remote_ssh(ip, password, cmd)
    logger.info(ret_data)
    return ret_code, ret_data


if __name__ == '__main__':
    ip = '127.0.0.1'
    password = '123456'

    import sys

    in_id = sys.argv[1]
    cid = sys.argv[2]
    out_id = sys.argv[3]
    deployFlow(ip, password, in_id, out_id, cid)

    # in_id=sys.argv[1]
    # cid=sys.argv[2]
    # flowUndeploy(ip,password,in_id,cid,'0')
