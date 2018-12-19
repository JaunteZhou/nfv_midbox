#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python 2.7
# RESTfulServer.py

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

import CenterUnit

app = Flask(__name__)
api = Api(app)

cu = CenterUnit.CenterUnit(["OpenStack", "Swarm", "OpenFlow", "SQLiteAgent"])
cu.print_clients()

class Abort(object):
    """Functions of Abort for Error Data Using"""

    def abort_if_list_doesnt_contain_id(self, l, i):
        if i not in l:
            abort(404, message="Todo {} doesn't exist".format(i))

    def abort_if_todo_doesnt_exist(self, todo_id):
        if todo_id not in TODOS:
            abort(404, message="Todo {} doesn't exist".format(todo_id))

    def abort_if_cloudnode_not_exist(self, service_node_id):
        if ostk_search_service_node(service_node_id) == False:
            abort(404, message="cloud node {} doesn't exist".format(service_node_id))

    def if__not_exist(self):
        pass


class NorthRESTfulAPI(Resource, Abort):
    """
    Interface Class for North RESTful API
    develop from class Resource and class Abort
    """
    def get(self):
        return "", 404

    def post(self):
        return "", 404

    def put(self):
        return "", 404

    def delete(self):
        return "", 404

# abort = Abort()

parser = reqparse.RequestParser()
parser.add_argument('task')

parser.add_argument('name')
parser.add_argument('vcpu')
parser.add_argument('mem')
parser.add_argument('disk')

parser.add_argument('security_function_id')
parser.add_argument('ability')
parser.add_argument('flow_match')

parser.add_argument('flow_table')

parser.add_argument('flow_name')

class Resource_CloudNode(NorthRESTfulAPI):
    def get(self, service_node_id):
        self.abort_if_cloudnode_doesnt_exist(service_node_id)
        return cu.proc(
            method = "GET", 
            south_agent = "OPENSTACK", 
            item = "CLOUD_NODE", 
            para = {"id":service_node_id})

class Resources_VM_Flavor(NorthRESTfulAPI):
    def get(self, flavor_id):
        return cu.proc(
            method = "GET", 
            south_agent = "OPENSTACK", 
            item = "FLAVOR", 
            para = {"id":flavor_id})

    def post(self):
        args = parser.parse_args()
        para = {
            'name': args['name'],
            'vcpu': args['vcpu'],
            'mem': args['mem'],
            'disk': args['disk']
        }
        return cu.proc(
            method = "POST", 
            south_agent = "OPENSTACK", 
            item = "FLAVOR", 
            para = para)

    def delete(self, flavor_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "OPENSTACK", 
            item = "FLAVOR", 
            para = {"id": flavor_id})

class Resources_VM_Image(NorthRESTfulAPI):
    def get(self, vm_image_id):
        return cu.proc(
            method = "GET", 
            south_agent = "OPENSTACK", 
            item = "IMAGE", 
            para = {"id":vm_image_id})

    def post(self, image_file_name):
        return cu.proc(
            method = "POST", 
            south_agent = "OPENSTACK", 
            item = "IMAGE", 
            para = {"image_file_name":image_file_name})

    def delete(self, vm_image_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "OPENSTACK", 
            item = "IMAGE", 
            para = {"vm_image_id":vm_image_id})

class Resources_Container_Image(NorthRESTfulAPI):
    def get(self, container_image_id):
        return cu.proc(
            method = "GET", 
            south_agent = "SWARM", 
            item = "IMAGE", 
            para = {"id":container_image_id})

    def post(self, image_file_name):
        return cu.proc(
            method = "POST", 
            south_agent = "SWARM", 
            item = "IMAGE", 
            para = {"image_file_name":image_file_name})

    def delete(self, container_image_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "SWARM", 
            item = "IMAGE", 
            para = {"container_image_id":container_image_id})

class Resources_SecurityFunction(NorthRESTfulAPI):
    def get(self, security_function_id):
        return cu.proc(
            method = "GET", 
            south_agent = "SECURITY_FUNCTION", 
            para = {"id":security_function_id})

    def delete(self, security_function_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "SECURITY_FUNCTION", 
            para = {"id":security_function_id})

class Running_CloudNode_FlowTable(NorthRESTfulAPI):
    def get(self, service_node_id):
        return cu.proc(
            method = "GET", 
            south_agent = "FLOWTABLE", 
            para = {"id":service_node_id})

    def post(self, service_node_id):
        args = parser.parse_args()
        para = {
            'id': service_node_id,
            'flow_table': args('flow_table')
        }
        return cu.proc(
            method = "POST", 
            south_agent = "FLOWTABLE", 
            para = para)

    def delete(self, service_node_id):
        args = parser.parse_args()
        para = {
            'id': service_node_id,
            'flow_name':args('flow_name')
        }
        return cu.proc(
            method = "DELETE", 
            south_agent = "FLOWTABLE", 
            para = para)

class Running_VM_instance(NorthRESTfulAPI):
    def get(self, vm_id):
        return cu.proc(
            method = "GET", 
            south_agent = "OPENSTACK", 
            item = "INSTANCE", 
            para = {"id":vm_id})

    def post(self, vm_id):
        args = parser.parse_args()
        para = {
            'vm_id': vm_id,
            'security_function_id':args('security_function_id'),
            'ability':args('ability'),
            'flow_match':args('flow_match')
        }
        return cu.proc(
            method = "POST", 
            south_agent = "OPENSTACK", 
            item = "INSTANCE", 
            para = para)

    def delete(self, vm_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "OPENSTACK", 
            item = "INSTANCE", 
            para = {"id":vm_id})

class Running_Container(NorthRESTfulAPI):
    def get(self, container_id):
        return cu.proc(
            method = "GET", 
            south_agent = "SWARM", 
            item = "CONTAINER", 
            para = {"id":container_id})

    def delete(self, container_id):
        return cu.proc(
            method = "DELETE", 
            south_agent = "SWARM", 
            item = "CONTAINER", 
            para = {"id":container_id})

class Running_CloudNode(NorthRESTfulAPI):
    def post(self, service_node_id):
        args = parser.parse_args()
        para = {
            'service_node_id': service_node_id,
            'security_function_id': args('security_function_id'),
            'ability': args('ability'),
            'flow_match': args('flow_match')
        }
        return cu.proc(
            method = "POST", 
            south_agent = "OPENSTACK", 
            item = "INSTANCE", 
            para = para)

class Running_Switch(NorthRESTfulAPI):
    def post(self, switch_id):
        args = parser.parse_args()
        para = {
            'switch_id': switch_id,
            'security_function_id':args('security_function_id'),
            'ability':args('ability'),
            'flow_match':args('flow_match')
        }
        return cu.proc(
            method = "POST", 
            south_agent = "OPENSTACK", 
            item = "INSTANCE", 
            para = para)


##
## Actually setup the Api resource routing here
##
api.add_resource(Resource_CloudNode, '/resource/cloudnode/<service_node_id>')

api.add_resource(Resources_VM_Flavor, '/resources/vm/flavor/<flavor_id>')
api.add_resource(Resources_VM_Flavor, '/resources/vm/flavor')

api.add_resource(Resources_VM_Image, '/resources/vm/image/<vm_image_id>')
api.add_resource(Resources_VM_Image, '/resources/vm/image/<image_file_name>')

api.add_resource(Resources_Container_Image, '/resources/container/image/<container_image_id>')
api.add_resource(Resources_Container_Image, '/resources/container/image/<image_file_name>')

api.add_resource(Resources_SecurityFunction, '/resources/security-function/<security_function_id>')

api.add_resource(Running_CloudNode_FlowTable, '/running/cloudnode/<service_node_id>/flow-table')

api.add_resource(Running_VM_instance, '/running/vm/instance/<vm_id>')

api.add_resource(Running_Container, '/running/container/<container_id>')

api.add_resource(Running_CloudNode, '/running/cloudnode/<service_node_id>')

api.add_resource(Running_Switch, '/running/switch/<switch_id>')


if __name__ == '__main__':
    app.run(debug=True)
