#!/usr/bin/python3
# -*- coding: utf-8 -*-
# openstack_para.py

import json
import time
from midbox._config import SERVERS_NAME_PREFIX, FLAVORS_ID_PREFIX, IMAGE_NAME_PREFIX, OPENSTACK_PORT_NAME_HEAD


def __get_time_stamp():
    now = int(round(time.time() * 1000))
    return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(now / 1000))


def makeFlavorId(vcpus, ram, disk):
    """Compose flavor id by vcpus, ram & disk."""
    return FLAVORS_ID_PREFIX + "-" + str(vcpus) \
           + "-" + str(ram) + "-" + str(disk)


def makeServerName():
    return SERVERS_NAME_PREFIX + "-" + __get_time_stamp()


def makeNewImageName():
    return IMAGE_NAME_PREFIX + "-" + __get_time_stamp()


def makePortNameInOvsById(port_id):
    return OPENSTACK_PORT_NAME_HEAD + port_id[0:11]


def composeServerPara(
        name, image_ref, flavor_ref, nets, same_host):
    """Compose JSON Param of Server Creatation."""
    para = {
        "server": {
            "name": name,
            "imageRef": image_ref,
            "flavorRef": flavor_ref,
            "networks": nets
        }
    }
    if same_host is not None:
        para["OS-SCH-HNT:scheduler_hints"] = {
            "same_host": same_host
        }
    return json.dumps(para)

def composeServerParaWithAZ(
        name, image_ref, flavor_ref, az, nets):
    """Compose JSON Param of Server Creatation."""
    para = {
        "server": {
            "name": name,
            "imageRef": image_ref,
            "flavorRef": flavor_ref,
            "availability_zone": az,
            "networks": nets
        }
    }
    return json.dumps(para)

def composeFlavorPara(id, name, vcpus, ram, disk):
    """Compose Param for Flavor Creatation."""
    req_dic = {
        "flavor": {
            "name": name,
            "vcpus": vcpus,
            "ram": ram,
            "disk": disk,
            "id": id
        }
    }
    return json.dumps(req_dic)


def composeCreateServerImagePara(new_image_name, metadata=None):
    # TODO:
    req_dic = {
        "createImage": {
            "name": new_image_name
        }
    }
    if metadata:
        req_dic["createImage"]["metadata"] = metadata
    return json.dumps(req_dic)


# def composeServerPara_oldVersion(
#         name, image_ref, flavor_ref, nets):
#     """Compose JSON Param of Server Creatation."""
#     para = {
#         "server":{
#             "name": name,
#             "imageRef": image_ref,
#             "flavorRef": flavor_ref,
#             "networks": nets
#         }
#     }
#     return json.dumps(para)


# do not use
def makePortsNameListInOVS(port_id_list):
    port_name_list_in_ovs = []
    for p_id in port_id_list:
        port_name_list_in_ovs.append(makePortNameInOvsById(p_id))
    return port_name_list_in_ovs


def composeNetworkPara(name="", mtu=1400, qos_policy_id=None):
    para = {
        "network": {
            "name": name,
            "admin_state_up": True,
            "mtu": mtu
        }
    }
    return json.dumps(para)


def composePortPara(name="", network_id=None, qos_policy_id=None):
    para = {
        "port": {
            "admin_state_up": True,
            "name": name,
            "network_id": network_id
        }
    }
    return json.dumps(para)


def composeInterfaceFixedIpsPara(net_id, ip_address):
    para = {
        "interfaceAttachment": {
            "fixed_ips": [
                {
                    "ip_address": ip_address
                }
            ],
            "net_id": net_id
        }
    }
    return json.dumps(para)


def composeInterfacePortsPara(port_id):
    para = {
        "interfaceAttachment": {
            "port_id": port_id
        }
    }
    return json.dumps(para)


def composeFloatingIpPara(port_id, floating_network_id):
    para = {
        "floatingip": {
            "port_id": port_id,
            "floating_network_id": floating_network_id
        }
    }
    return json.dumps(para)


def composeServerInstanceDictPara(vcpus, ram, disk, image_id, host_id):
    para = {
        "vcpus": vcpus,
        "ram": ram,
        "disk": disk,
        "image_id": image_id,
        "host_id": host_id
    }
    return para
