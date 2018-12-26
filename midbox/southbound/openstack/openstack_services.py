#!/usr/bin/python3
# -*- coding: utf-8 -*-
#openstack_services.py
import logging
logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import servers, flavor, image, networking, ports, volume, floating_ips, hypervisors
from midbox.southbound.openstack.openstack_rest_api.openstack_config import public_net_id, private_net_id, data_flow_net_id, private_net_name, data_flow_net_name, SLEEP_SECONDS_IN_ATTACHING
from midbox.southbound.openstack import openstack_para
import time

########## Instance(Nova) ##########
def addServerInstance(vcpus, ram, disk, image_id, host_id):
    logger.debug('Start.')
    # get Flavor ID
    f_id = addFlavor(vcpus, ram, disk)
    if f_id == -1:
        logger.error("Add or Get Flavor.")
        return -1

    same_host = getSameHostInstanceId(host_id)
    # server
    if same_host == None:
        para_json = openstack_para.composeServerPara(
                openstack_para.makeServerName(),
                image_id,
                f_id,
                [{"uuid":private_net_id}])
    else:
        para_json = openstack_para.composeServerParaWithSameHost(
                openstack_para.makeServerName(),
                image_id,
                f_id,
                [{"uuid":private_net_id}],
                same_host)
    s_ret = servers.createServer(para_json)
    if s_ret == -1:
        logger.error("Create New Server.")
        return -1
    s_id = s_ret["id"]

    # create Volume and get Volume ID
    v_ret = volume.createVolume(disk)
    if v_ret == None:
        logger.error("Create Volume.")
        return -1
    v_id = v_ret["id"]

    return {"serverId": s_id, "volumeId": v_id}

def delServerInstance(s_id, vol_clear=True):
    logger.debug('Start.')
    err_list = []
    # get server's attachments
    vol_list = servers.getVolumeAttachments(s_id)
    logger.debug(("Volumes List: " + vol_list))
    # detach all volumes in server's attachments
    for i in range(len(vol_list)):
        logger.debug(("server id: ", vol_list[i]["serverId"]))
        logger.debug(("volume id: ", vol_list[i]["volumeId"]))
        ret = servers.detachVolume(vol_list[i]["serverId"], vol_list[i]["volumeId"])
        logger.debug(("Return of Detach Volume: ", ret))
        if ret != True:
            err_list.append({vol_list[i]["volumeId"]: ret})

    # delete floating ip
    logger.debug("delete floating ip")
    floating_id = ""
    ports_id_list = getServerInterfacesIdByNet(s_id, private_net_name)
    logger.debug(("ports_id_list: ", ports_id_list))
    floating_ips_list = floating_ips.getFloatingIpsList()
    logger.debug(("floating_ips_list: ", floating_ips_list))
    for f_ip in floating_ips_list:
        if f_ip["port_id"] in ports_id_list:
            floating_id = f_ip["id"]
            break
    if floating_id != "":
        floating_ips.deleteFloatingIp(floating_id)

    # save ports list
    logger.debug("get server interfaces list")
    ports_list = getAllServerInterfaces(s_id)
    logger.debug(("ports_list: ", ports_list))

    # delete server
    logger.debug("delete server")
    ret = servers.deleteServer(s_id)
    logger.debug(("return of delete Server: ", ret))
    RuntimeWarning# delete all volumes
    if vol_clear == True:
        logger.debug("Start Clear Volume !")

        for i in range(len(vol_list)):
            logger.debug(("volume id: ", vol_list[i]["volumeId"]))
            ret = volume.deleteVolume(vol_list[i]["volumeId"])
            logger.debug(("return of delete volume: ", ret))
            if ret != True:
                err_list.append({vol_list[i]["volumeId"]:ret})

    # delete ports list
    logger.debug("delete ports list")
    for port in ports_list:
        ret = ports.deletePort(port)
        logger.debug(("return of delete port: ", ret))

    return True

def attachingServerVolumeList(sv_list):
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

def attachingServerPortList(sv_list, ports_list):
    logger.debug('Start.')
    key_list = range(len(sv_list))
    tmp = []
    while len(key_list):
        for i in key_list:
            p_id = ports_list.pop()
            para_json = openstack_para.composeInterfacePortsPara(p_id)
            ret = servers.attachPortInterfaces(
                    sv_list[i]["serverId"], para_json)
            if ret == -1:
                logger.debug("Failed to Attach Ports to Server. Maybe try next time.")
                tmp.append(i)
                ports_list.append(p_id)
        key_list = tmp
    return ports_list

########## Flavor(Nova) ##########
def addFlavor(vcpus, ram, disk):
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
    code, res = flavor.createFlavor(para_json)
    if code == 200:
        return f_id
    else:
        # TODO: log
        return -1


########## Networking(Neutron) ##########
def getNetworkIdByName(name):
    logger.debug('Start.')
    nets = networking.getNetworksList()
    for n in nets:
        if n["name"] == name:
            return n["id"]

def getServerInterfacesIdByNet(s_id, net_name):
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

def getAllServerInterfaces(s_id):
    logger.debug('Start.')
    server_detail = servers.getServerDetail(s_id)
    # get mac address list from server details
    mac_list = []
    for key in server_detail["addresses"].keys():
        for iface in server_detail["addresses"][key]:
            mac_list.append(iface["OS-EXT-IPS-MAC:mac_addr"])
    mac_set = set(mac_list)
    # get ports' id list by comparing mac address in mac_list
    ports_list = ports.getPortsList()
    ports_id_list = []
    for port in ports_list:
        if port["mac_address"] in mac_set:
            ports_id_list.append(port["id"])
    return list(set(ports_id_list))

def createDoublePorts(net_name=data_flow_net_name, net_id=""):
    logger.debug('Start.')
    net_id = getNetworkIdByName(net_name)
    return createNPorts(2, net_id)

def createNPorts(n, net_id):
    logger.debug('Start.')
    ports_list = []
    for i in range(n):
        para_json = openstack_para.composePortPara(network_id=net_id)
        port = ports.createPort(para_json)
        if port == None:
            logger.error("Creating " + str(i+1) + "th Port in " + str(n) + " Ports.")
            for pi in ports_list:
                ports.deletePort(pi)
            return None
        ports_list.append(port["id"])
    return ports_list


def getSameHostInstanceId(host_id):
    logger.debug('Start.')
    host_list = hypervisors.getHostsList()
    host_name = ''
    for host in host_list:
        if host['id'] == host_id:
            host_name = host['hypervisor_hostname']
    if host_name == '':
        return None
    
    servers_list = servers.getServersListDetails()
    for s in servers_list:
        if s['OS-EXT-SRV-ATTR:hostname'] == host_name:
            return s['id']
    return None


def getVmInterfacesNameInDataPlane(server_id):
    logger.debug('Start.')
    ports_id_list = getServerInterfacesIdByNet(server_id, private_net_name)
    port_name_list_in_ovs = []
    for port_id in ports_id_list:
        port_name_list_in_ovs.append(
                openstack_para.makePortNameInOvsById(port_id))
    return port_name_list_in_ovs

########## SFC ##########
def addVm(para):
    logger.debug('Start.')
    ret = addVmsList([para])
    # TODO: 错误处理
    return ret[0]

def delVm(server_id):
    logger.debug('Start.')
    ret = delServerInstance(server_id)
    # TODO: 错误处理
    return ret

def addVmsList(para_list=[]):
    """
    para_list = [
        {
            "vcpus": 1,
            "ram": 256,
            "disk": 1,
            "image_id": "xxxx-xx-xx-xxxx",
            "same_host": "xxxx-xx-xx-xxxx"
        },{...},{...}
    ]
    """
    logger.debug('Start.')
    sv_list = []
    for para in para_list:
        sv = addServerInstance(
                para["vcpus"],
                para["ram"],
                para["disk"],
                para["image_id"],
                para["host_id"])
        # logger.debug(sv)
        if sv == -1:
            logger.error("Add Server Instance.")
            continue
        para["server_id"] = sv["serverId"]
        para["volume_id"] = sv["volumeId"]
        sv_list.append(sv)

    tmp = attachingServerVolumeList(sv_list)
    while len(tmp):
        for sv_pair in tmp:
            logger.debug(("serverId: ", sv_pair["serverId"]))
            logger.debug(("volumeId: ", sv_pair["volumeId"]))
        tmp = attachingServerVolumeList(tmp)
        if len(tmp) != 0:
            time.sleep(SLEEP_SECONDS_IN_ATTACHING)

    # set floating ip to port in private_net
    for para in para_list:
        s_id = para["server_id"]
        port_list = getServerInterfacesIdByNet(s_id, private_net_name)
        if len(port_list) != 1:
            logger.error("Find Server Port.")
            continue
        p_id = port_list[0]
        floatingip_para = openstack_para.composeFloatingIpPara(p_id, public_net_id)
        floatingip_ret = floating_ips.createFloatingIp(floatingip_para)
        if floatingip_ret == -1:
            logger.error("Set Floating IP.")
            continue
        para["ip_address"] = floatingip_ret["floating_ip_address"]

    # create 2N ports and attach them to server
    ports_list = createNPorts(len(para_list)*2, getNetworkIdByName(data_flow_net_name))
    
    logger.debug(ports_list)
    ports_2_list = attachingServerPortList(sv_list, ports_list)
    logger.debug(ports_list)
    attachingServerPortList(sv_list, ports_2_list)

    return para_list



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