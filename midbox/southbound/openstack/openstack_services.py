#!/usr/bin/python3
# -*- coding: utf-8 -*-
# openstack_services.py
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import servers, flavor, image, networking, ports, volume, floating_ips, hypervisors
from midbox._config import private_net_id, private_net_name, data_in_net_id, data_in_net_name, data_out_net_id, data_out_net_name, SLEEP_SECONDS_IN_ATTACHING
from midbox.southbound.openstack import openstack_para
import time


def addVm(vcpus, ram, disk, image_id, host_id):
    logger.debug('Start.')
    sv = add_server_instance(vcpus, ram, disk, image_id, host_id)
    if sv is None:
        return None

    # 将磁盘挂接实例
    tmp = __attaching_server_volume_list([sv])
    while len(tmp):
        for sv_pair in tmp:
            logger.debug(("serverId: ", sv_pair["serverId"]))
            logger.debug(("volumeId: ", sv_pair["volumeId"]))
        tmp = __attaching_server_volume_list(tmp)
        if len(tmp) != 0:
            time.sleep(SLEEP_SECONDS_IN_ATTACHING)
    mng_port = __get_vm_mng_ports_name(sv['serverId'])
    sv['manPortName'] = mng_port
    ports_list = getVmDataInAndOutPortsName(sv['serverId'])
    sv['dataPortsNameList'] = ports_list
    return sv


def delVm(server_id):
    logger.debug('Start.')
    ret = del_server_instance(server_id)
    return ret


def add_server_instance(vcpus, ram, disk, image_id, host_id):
    logger.debug('Start.')
    # get Flavor ID
    f_id = add_flavor(vcpus, ram, disk)
    if f_id == -1:
        logger.error("Add or Get Flavor.")
        return None

    same_host = __get_any_instance_id_in_same_host(host_id)

    para_json = openstack_para.composeServerPara(
            openstack_para.makeServerName(),
            image_id,
            f_id,
            [
                {"uuid":private_net_id},
                {"uuid":data_in_net_id},
                {"uuid":data_out_net_id}
            ],
            same_host)

    s_ret = servers.createServer(para_json)
    if s_ret == -1:
        logger.error("Create New Server.")
        return None
    s_id = s_ret["id"]

    # create Volume and get Volume ID
    v_ret = volume.createVolume(disk)
    if v_ret is None:
        logger.error("Create Volume.")
        return None
    v_id = v_ret["id"]

    return {"serverId": s_id, "volumeId": v_id}


def del_server_instance(s_id, vol_clear=True):
    logger.debug('Start.')
    err_list = []
    # get server's attachments
    vol_list = servers.getVolumeAttachments(s_id)
    logger.debug(("Volumes List: ", vol_list))
    # detach all volumes in server's attachments
    for i in range(len(vol_list)):
        logger.debug(("server id: ", vol_list[i]["serverId"]))
        logger.debug(("volume id: ", vol_list[i]["volumeId"]))
        ret = servers.detachVolume(vol_list[i]["serverId"], vol_list[i]["volumeId"])
        if ret is not True:
            logger.error(("Detach Volume: ", ret))
            err_list.append({vol_list[i]["volumeId"]: ret})
        logger.debug(("Detach Volume: ", ret))

    # get ports list
    logger.debug("Start Getting Server Interfaces List")
    ports_list = __get_all_server_interfaces(s_id)
    logger.debug(("Ports_List: ", ports_list))

    # delete server
    logger.debug("Delete Server")
    ret = servers.deleteServer(s_id)
    logger.debug(("Delete Server: ", ret))

    # delete ports list
    logger.debug("Delete Ports List")
    for port in ports_list:
        ret = ports.deletePort(port)
        logger.debug(("Return of Delete Port: ", ret))
        if ret is not True:
            err_list.append({port:ret})
    
    # delete all volumes
    if vol_clear is True:
        logger.debug("Start Clear Volume !")

        for i in range(len(vol_list)):
            logger.debug(("Volume Id: ", vol_list[i]["volumeId"]))
            ret = volume.deleteVolume(vol_list[i]["volumeId"])
            logger.debug(("Return of Delete Volume: ", ret))
            if ret is not True:
                err_list.append({vol_list[i]["volumeId"]:ret})

    if len(err_list) != 0:
        return False
    return True


def add_flavor(vcpus, ram, disk):
    """Get a flavor id."""
    logger.debug('Start.')
    # get f_id of flavor requested
    f_id = openstack_para.makeFlavorId(vcpus, ram, disk)
    # init dictinary of new flavor's para
    f_list = flavor.getFlavorsList()
    # check whether flavor by f_id is existed
    for f in f_list:
        if f["id"] == f_id:
            return f_id
    # if flavor by f_id is not existed, create flavor by f_id
    para_json = openstack_para.composeFlavorPara(f_id, f_id, vcpus, ram, disk)
    ret = flavor.createFlavor(para_json)
    if ret is True:
        return f_id
    else:
        logger.error("Create Flavor.")
        return -1


def getVmDataInAndOutPortsName(s_id):
    logger.debug('Start.')
    ports_name_list = []
    # 获取vm的端口信息
    in_port_id_list = __get_server_interfaces_id_list_by_net_name(s_id, data_in_net_name)
    if len(in_port_id_list) == 0:
        return None
    ports_name_list.append(
                openstack_para.makePortNameInOvsById(in_port_id_list[0]))
    # vm在外部端口编号
    out_port_id_list = __get_server_interfaces_id_list_by_net_name(s_id, data_out_net_name)
    if len(out_port_id_list) == 0:
        return None
    ports_name_list.append(
                openstack_para.makePortNameInOvsById(out_port_id_list[0]))
        
    return ports_name_list


# def addVmsList(para_list=[]):
#     """
#     para_list = [
#         {
#             "vcpus": 1,
#             "ram": 256,
#             "disk": 1,
#             "image_id": "xxxx-xx-xx-xxxx",
#             "same_host": "xxxx-xx-xx-xxxx"
#         },{...},{...}
#     ]
#     """
#     logger.debug('Start.')
#     sv_list = []
#     for para in para_list:
#         sv = addServerInstance(
#                 para["vcpus"],
#                 para["ram"],
#                 para["disk"],
#                 para["image_id"],
#                 para["host_id"])
#         if sv == -1:
#             logger.error("Add Server Instance.")
#             continue
#         para["server_id"] = sv["serverId"]
#         para["volume_id"] = sv["volumeId"]
#         sv_list.append(sv)
#
#     # attaching servers to volumes by list
#     tmp = __attaching_server_volume_list(sv_list)
#     while len(tmp):
#         for sv_pair in tmp:
#             logger.debug(("serverId: ", sv_pair["serverId"]))
#             logger.debug(("volumeId: ", sv_pair["volumeId"]))
#         tmp = __attaching_server_volume_list(tmp)
#         if len(tmp) != 0:
#             time.sleep(SLEEP_SECONDS_IN_ATTACHING)
#
#     return para_list


def __get_net_id_by_net_name(net_name):
    logger.debug('Start.')
    nets = networking.getNetworksList()
    for n in nets:
        if n["name"] == net_name:
            return n["id"]
    return None


def __get_server_interfaces_id_list_by_net_name(s_id, net_name):
    logger.debug('Start.')
    server_detail = servers.getServerDetail(s_id)
    # get mac address list from server details
    mac_list = []
    for iface in server_detail["addresses"][net_name]:
        mac_list.append(iface["OS-EXT-IPS-MAC:mac_addr"])
    mac_set = set(mac_list)
    # get ports' id list by comparing mac address in mac_list
    ports_list = ports.getPortsList()
    ports_id_list = []
    for port in ports_list:
        if port["mac_address"] in mac_set:
            ports_id_list.append(port["id"])
    return list(set(ports_id_list))


def __get_all_server_interfaces(s_id):
    logger.debug('Start.')
    server_detail = servers.getServerDetail(s_id)
    # get mac address list from server details
    mac_list = []
    for key in server_detail["addresses"].keys():
        for iface in server_detail["addresses"][key]:
            mac_list.append(iface["OS-EXT-IPS-MAC:mac_addr"])
    mac_set = set(mac_list)
    logger.debug(mac_set)
    # get ports' id list by comparing mac address in mac_list
    ports_list = ports.getPortsList()
    ports_id_list = []
    for port in ports_list:
        if port["mac_address"] in mac_set:
            ports_id_list.append(port["id"])
    logger.debug(ports_id_list)
    return list(set(ports_id_list))


def __get_any_instance_id_in_same_host(host_id):
    logger.debug('Start.')
    host_list = hypervisors.getHostsList()
    host_name = ''
    for host in host_list:
        if str(host['id']) == str(host_id):
            host_name = host['hypervisor_hostname']
    if host_name == '':
        return None
    logger.debug(('Host Name', host_name))
    servers_list = servers.getServersListDetails()
    for s in servers_list:
        if s['OS-EXT-SRV-ATTR:hypervisor_hostname'] == host_name:
            logger.debug(('Any Server Id', s['id']))
            return s['id']
    return None


def __get_vm_mng_ports_name(s_id):
    logger.debug('Start.')
    # port used managing vm
    man_port_id_list = __get_server_interfaces_id_list_by_net_name(s_id, private_net_name)
    if len(man_port_id_list) == 0:
        return None
    man_port_name = openstack_para.makePortNameInOvsById(man_port_id_list[0])

    return man_port_name


def __attaching_server_volume_list(sv_list):
    logger.debug('Start.')
    new_list = []
    logger.debug("Attaching...")
    for i in range(len(sv_list)):
        s = servers.getServerDetail(sv_list[i]["serverId"])
        if s["status"] == "ACTIVE":
            ret, res = servers.attachVolume(
                    sv_list[i]["serverId"], sv_list[i]["volumeId"])
            if ret == False:
                logger.error(res)
                new_list.append(sv_list[i])
        else:
            new_list.append(sv_list[i])
    return new_list


# def attachingServerPortList(sv_list, ports_list):
#     logger.debug('Start.')
#     key_list = range(len(sv_list))
#     tmp = []
#     while len(key_list):
#         for i in key_list:
#             p_id = ports_list.pop()
#             para_json = openstack_para.composeInterfacePortsPara(p_id)
#             ret = servers.attachPortInterfaces(
#                     sv_list[i]["serverId"], para_json)
#             if ret == -1:
#                 logger.debug("Failed to Attach Ports to Server. Maybe try next time.")
#                 tmp.append(i)
#                 ports_list.append(p_id)
#         key_list = tmp
#     return ports_list


if __name__ == '__main__':
    # # centos_image_id = "843e7950-e0d7-402f-80b5-6a1c3805708d"
    # cirros_image_id = "7a6da8f1-c3e9-42dd-88d2-ffe9084d3b24"
    # host_id = 1
    # para1 = openstack_para.composeServerInstanceDictPara(1, 256, 1, cirros_image_id, host_id)
    # # para2 = openstack_para.composeServerInstanceDictPara(1, 1024, 10, centos_image_id, host_id)
    # p_list = []
    # p_list.append(para1)
    # # p_list.append(para2)
    # logger.debug(addVmsList(para_list=p_list))


    # ret = ports.getPortsList()
    # logger.debug(ret)


    # delServerInstance("e728988d-2ff1-46e5-83dc-ea11dad2f86f")
    # ret = ports.deletePort('5ddbf8e0-105b-4169-8ac5-2be6d362a083')
    # logger.debug("return of delete port: ", ret)


    # logger.debug(volume.createVolume(1))
    # logger.debug(volume.getVolumesList())
    # logger.debug(volume.deleteVolume('076eb635-8a47-4053-bc3e-a7b3e7c65c58'))


    # logger.debug(floating_ips.deleteFloatingIp("0f8cd16b-364c-44ca-ba80-c10e243b96f7"))
    # logger.debug(floating_ips.getFloatingIpsList())

    print(hypervisors.getHostsListDetails())

    # logger.debug (servers.getServersListDetails())

    pass