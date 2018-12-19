#!/bin/python
import json
import time

SERVERS_ID_PREFIX = "S"
FLAVORS_ID_PREFIX = "F"

def getTimestamp():
    now = int(round(time.time()*1000))
    return time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(now/1000))

def makeFlavorId(vcpus, ram, disk):
    """Compose flavor id by vcpus, ram & disk."""
    return FLAVORS_ID_PREFIX \
            + "-" + str(vcpus) \
            + "-" + str(ram) \
            + "-" + str(disk)

def makeServerName():
    return SERVERS_ID_PREFIX + "-" + getTimestamp()

def makePortNameInOVS(name):
    return "tap" + name[0:11]

def makePortsNameListInOVS(port_id_list):
    port_name_list_in_ovs = []
    for p_id in port_id_list:
        port_name_list_in_ovs.append(makePortNameInOVS(p_id))
    return port_name_list_in_ovs

########## Para ##########
### Server ###
def composeServerPara(
        name, image_ref, flavor_ref, nets, same_host):
        #port_1, port_2, port_3):
    """Compose JSON Param of Server Creatation."""
    para = {
        "server":{
            "name": name,
            "imageRef": image_ref,
            "flavorRef": flavor_ref,
            "networks": nets
        },
        "OS-SCH-HNT:scheduler_hints": {
            "same_host": same_host
        }
    }
    return json.dumps(para)

def composeServerPara_old(
        name, image_ref, flavor_ref, nets):
    """Compose JSON Param of Server Creatation."""
    para = {
        "server":{
            "name": name,
            "imageRef": image_ref,
            "flavorRef": flavor_ref,
            "networks": nets
        }
    }
    return json.dumps(para)

def composeFlavorPara(id, name, vcpus, ram, disk):
    """Compose Param for Flavor Creatation."""
    req_dic = {
        "flavor":{
            "name": name,
            "vcpus": vcpus,
            "ram": ram,
            "disk": disk,
            "id": id
        }
    }
    return json.dumps(req_dic)

### Networking ###
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

def composeFloatingIpPara(port_id,floating_network_id):
    para = {
        "floatingip": {
            "port_id": port_id,
            "floating_network_id": floating_network_id
        }
    }
    return json.dumps(para)

### Instance ###
def composeServerInstancePara(vcpus, ram, disk, image_id, same_host):
    para = {
        "vcpus": vcpus,
        "ram": ram,
        "disk": disk,
        "image_id": image_id
    }
    if same_host == "":
        para["same_host"] = same_host
    return para