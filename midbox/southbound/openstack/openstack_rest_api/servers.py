#!/usr/bin/python3
# -*- coding: utf-8 -*-
# servers.py
"""This module provides a series of openstack compute APIs"""
import json
import requests
import logging

logger = logging.getLogger(__name__)

from midbox.southbound.openstack.openstack_rest_api import rest_requests
from midbox._config import servers_url

"""
The possible server status values are:
ACTIVE. The server is active.
BUILD. The server has not finished the original build process.
DELETED. The server is permanently deleted.
ERROR. The server is in error.
HARD_REBOOT. The server is hard rebooting. This is equivalent to pulling the power plug on a physical server, plugging it back in, and rebooting it.
MIGRATING. The server is being migrated to a new host.
PASSWORD. The password is being reset on the server.
PAUSED. In a paused state, the state of the server is stored in RAM. A paused server continues to run in frozen state.
REBOOT. The server is in a soft reboot state. A reboot command was passed to the operating system.
REBUILD. The server is currently being rebuilt from an image.
RESCUE. The server is in rescue mode. A rescue image is running with the original server image attached.
RESIZE. Server is performing the differential copy of data that changed during its initial copy. Server is down for this stage.
REVERT_RESIZE. The resize or migration of a server failed for some reason. The destination server is being cleaned up and the original source server is restarting.
SHELVED: The server is in shelved state. Depending on the shelve offload time, the server will be automatically shelved offloaded.
SHELVED_OFFLOADED: The shelved server is offloaded (removed from the compute host) and it needs unshelved action to be used again.
SHUTOFF. The server is powered off and the disk image still persists.
SOFT_DELETED. The server is marked as deleted but the disk images are still available to restore.
SUSPENDED. The server is suspended, either by request or necessity. This status appears for only the XenServer/XCP, KVM, and ESXi hypervisors. Administrative users can suspend an instance if it is infrequently used or to perform system maintenance. When you suspend an instance, its VM state is stored on disk, all memory is written to disk, and the virtual machine is stopped. Suspending an instance is similar to placing a device in hibernation; memory and vCPUs become available to create other instances.
UNKNOWN. The state of the server is unknown. Contact your cloud provider.
VERIFY_RESIZE. System is awaiting confirmation that the server is operational after a move or resize.
"""


def getServersList():
    """
    Get list of servers.
    :return:[
                {
                    "id": "22c91117-08de-4894-9aa9-6ef382400985",
                    "name": "new-server-test"
                },{...},{...}
            ]
    """
    code, res = rest_requests.get(servers_url)
    if code != requests.codes.ok:
        logger.error((code, res))
        return code

    sl = res["servers"]
    for i in range(len(sl)):
        sl[i].pop("links")
    return sl
    # Normal response codes: 200
    # Error response codes: badRequest(400), unauthorized(401), forbidden(403)


def getServersListDetails():
    """
    Get list of servers with details.
    """
    code, res = rest_requests.get(servers_url + "/detail")
    if code != requests.codes.ok:
        logger.error((code, res))
        return code
    sl = res["servers"]
    for i in range(len(sl)):
        sl[i].pop("links")
    return sl


def getServerDetail(s_id):
    """Get server by id with details."""
    code, res = rest_requests.get(servers_url + "/" + s_id)
    if code != requests.codes.ok:
        logger.error((code, res))
        return code
    sl = res["server"]
    sl.pop("links")
    return sl


def createServer(para_json):
    """Create a new server with json-formed para."""
    code, res = rest_requests.post(servers_url, para_json)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return -1
    return res["server"]


def deleteServer(s_id):
    """
    Delete a Server by id.
    Normal Return: True
    Error Return: False
    """
    code, res = rest_requests.delete(servers_url + "/" + s_id)
    if code != requests.codes.no_content:
        logger.error((code, res))
        return False
    return True
    # Normal response codes: 204
    # Error response codes: unauthorized(401), forbidden(403), itemNotFound(404), conflict(409)


### Create Image ###
def createImage(s_id, para_json):
    code, res = rest_requests.post(servers_url + "/" + s_id + "/action", para_json)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return -1
    # TODO:
    print(res)
    return res["image_id"]


### Volume Attachments ###
def getVolumeAttachments(s_id):
    """Get Volume Attachment to Server by id."""
    code, res = rest_requests.get(servers_url + "/" + s_id + "/os-volume_attachments")
    if code != requests.codes.ok:
        logger.error((code, res))
        return []
    return res["volumeAttachments"]


def attachVolume(s_id, vol_id):
    """
    Attach Volume to Server by id.
    res : {
        "volumeAttachment": {
            "device": "/dev/vdd",
            "id": "xxx",
            "serverId": "xxx",
            "volumeId": "xxx"
        }
    }
    """
    para_dic = {
        "volumeAttachment": {
            "volumeId": vol_id
        }
    }
    para_json = json.dumps(para_dic)
    code, res = rest_requests.post(
        servers_url + "/" + s_id + "/os-volume_attachments",
        para_json)
    if code != requests.codes.ok:
        logger.error((code, res))
        return False, res
    return True, res["volumeAttachment"]


def detachVolume(s_id, vol_id):
    """Detach Volume to Server by id."""
    code, res = rest_requests.delete(
        servers_url + "/" + s_id + "/os-volume_attachments/" + vol_id)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return False
    return True


### Ports interfaces ###
def getPortInterfaces(s_id):
    code, res = rest_requests.get(
        servers_url + "/" + s_id + "/os-interface")
    if code != requests.codes.ok:
        logger.error((code, res))
        return res
    return res["interfaceAttachments"]


def attachPortInterfaces(s_id, para_json):
    code, res = rest_requests.post(
        servers_url + "/" + s_id + "/os-interface",
        para_json)
    if code != requests.codes.ok:
        logger.error((code, res))
        return -1
    # print (res)
    return res["interfaceAttachment"]


def getPortInterfacesDetails(s_id, p_id):
    code, res = rest_requests.get(
        servers_url + "/" + s_id + "/os-interface/" + p_id)
    if code != requests.codes.ok:
        logger.error((code, res))
        return res
    return res["interfaceAttachments"]


def detachPortInterfaces(s_id, p_id):
    code, res = rest_requests.delete(
        servers_url + "/" + s_id + "/os-interface/" + p_id)
    if code != requests.codes.accepted:
        logger.error((code, res))
        return res
    return True


if __name__ == '__main__':
    print("port interfaces list: ", getPortInterfaces("ca17b74c-3ee9-4fbc-bea6-c21ce7d16abf"))
    # print ("server ip addr:", s.getServerIP('85bdb339-6dc7-4de0-8fa1-1dce6bd942eb'))

    # print ("flavors list: ", f.getFlavorsList())

    # f = flavors()
    # print ("flavors list: ", f.getFlavorId(1, 256, 1))

    # h = hypervisor()
    # print ("hosts list: ", h.get_hosts_detail())

    # su = SimpleUsage()
    # print(su.getAllSimpleTenantUsage(1))
