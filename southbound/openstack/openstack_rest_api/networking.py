"""This module provides a series of openstack networkding APIs"""
import sys
sys.path.append(r"/Users/JaunteZhou/Documents/NFV30py/nfv30py")
import json

import rest_requests
from openstack_config import networks_url

def getNetworksList():
    """Get list of Networks."""
    code, res = rest_requests.get(networks_url)
    if code != 200:
        # TODO: log
        return None
    return res["networks"]

def createNetwork(para_json):
    """Create a Network."""
    code, res = rest_requests.post(networks_url, para_json)
    if code != 201:
        # TODO: log
        print (res)
        return None
    return res["network"]

def updateNetwork(id, para_json):
    """Update a Network."""
    code, res = rest_requests.put(networks_url + "/" + id, para_json)
    if code != 200:
        # TODO: log
        return None
    return res["network"]

def deleteNetwork(id):
    """Delete a Network."""
    code, res = rest_requests.get(networks_url + "/" + id)
    if code != 204:
        # TODO: log
        return False
    return True

### Trunk networking
### Router
### Subnet
### Firewall '/fwaas'

if __name__ == '__main__':
    # n = Networking()
    # print(n.getNetworksList())

    # nets = getNetworksList()
    # print (li)
    # for n in nets:
    #     print (n)
    #     print (n["name"])
    #     if n["name"] == "net_ctrl_plane":
    #         print (n["id"])

    # json_para = composeNetworkPara(name="data_net")
    para = {
        "network": {
            "admin_state_up": True,
            "name": "net1",
            "provider:network_type": "flat",
            "provider:segmentation_id": 2
        }
    }
    json_para = json.dumps(para)
    print (createNetwork(json_para))