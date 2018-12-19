#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python 2.7
# CenterUnit.py

import json
# import urllib2

import OpenStackAgent
import SwarmAgent
import OpenFlowAgent
import SQLiteAgent

class CenterUnit(object):

    def __init__(self, agents):#, north_server="REST"):
        # init kinds of agents object
        kinds_of_agents = {
            "OpenStack": OpenStackAgent.OpenStackAgent, 
            "Swarm": SwarmAgent.SwarmAgent,
            "OpenFlow": OpenFlowAgent.OpenFlowAgent,
            "SQLite": SQLiteAgent.SQLiteAgent
        }
        # kinds_of_servers = {"REST":RESTfulServer}

        # init self.agents for needs
        self.agents = {}
        for cli in agents:
            print(cli)
            if kinds_of_agents.get(cli) == None:
                print("This kind of object have not signed in.")
                continue
            o_cli = kinds_of_agents.get(cli)()
            self.agents[cli] = o_cli

        ### TODO 
        # Start NorthRESTful Server
        # if north_server == "REST":
        #     test_restful.app.run()


    def print_clients(self):
        print(self.agents)
        for cli in self.agents:
            print(cli)

    def __show_security_function(self, para):
        """
        功能：完成从安全功能到对应虚拟机镜像或容器镜像的映射
        参数：
            para：包含安全功能编号的字典
        """
        south_agent, rsc_id = self.agents["SQLite"].search(para["id"])
        # find image of security function
        return do_get("SHOW", south_agent, "IMAGE", {"id": rsc_id})

    def __delete_security_function(self, para):
        """
        功能：完成从安全功能到对应虚拟机镜像或容器镜像的映射
        参数：
            para：包含安全功能编号的字典
        """
        south_agent, rsc_id = self.agents["SQLite"].search(para["id"])
        # del image of security function
        return do_delete("DELETE", south_agent, "IMAGE", {"id": rsc_id})  # or name


    def proc(self, method, south_agent, item = "", para):
        """
        功能：核心处理函数，完成函数之间的映射
        参数：
            method：字符串，请求处理的方式，有SHOW，ADD，DELETE，可添加UPDATE
            south_agent：字符串，南向服务代理
            item：字符串，请求处理的元素，镜像、容器、虚拟机等等
            para：字典类型，输入参数
        """
        func = {
            "GET" : {
                "OPENSTACK":{
                    "CLOUD_NODE": self.agents["OpenStack"].show_node,
                    "FLAVOR": self.agents["OpenStack"].show_flavor,
                    "IMAGE": self.agents["OpenStack"].show_image,
                    "INSTANCE": self.agents["OpenStack"].show_instance,
                },
                "SWARM":{
                    "IMAGE": self.agents["Swarm"].show_image,
                    "CONTAINER": self.agents["Swarm"].show_container
                },
                "FLOWTABLE": {
                    "": self.agents["OpenFlow"].show_flowtable
                },
                "SECURITY_FUNCTION": {
                    "": __show_security_function
                }
            }
            "POST" : {
                "OPENSTACK":{
                    "CLOUD_NODE": self.agents["OpenStack"].add_node,
                    "FLAVOR": self.agents["OpenStack"].add_flavor,
                    "IMAGE": self.agents["OpenStack"].add_image,
                    "INSTANCE": self.agents["OpenStack"].add_instance,
                },
                "SWARM":{
                    "IMAGE": self.agents["Swarm"].add_image,
                    "CONTAINER": self.agents["Swarm"].add_container
                },
                "FLOWTABLE": {
                    "": self.agents["OpenFlow"].add_flowtable
                # },
                # "SECURITY_FUNCTION": {
                #     "": __add_security_function
                }
            }
            "DELETE" : {
                "OPENSTACK":{
                    #"CLOUD_NODE": self.agents["OpenStack"].delete_node,
                    "FLAVOR": self.agents["OpenStack"].delete_flavor,   # name or id
                    "IMAGE": self.agents["OpenStack"].delete_vm_image,  # name or id
                    "INSTANCE": self.agents["OpenStack"].delete_instance,
                },
                "SWARM":{
                    "IMAGE": self.agents["Swarm"].delete_image,   # name or id
                    "CONTAINER": self.agents["Swarm"].delete_container
                },
                "FLOWTABLE": {
                    "": self.agents["OpenFlow"].delete_flowtable
                }
                "SECURITY_FUNCTION": {
                    "": __delete_security_function
                }
            }
        }
        return func[method][south_agent][item](para)


if __name__ == '__main__':
    a = CenterUnit(["OpenStack", "Swarm", "OpenFlow", "SQLiteAgent"])
    a.print_clients()
    # a.clients["OpenStack"] = ""
    # a.print_clients()