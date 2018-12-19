#!/bin/python
# python 2.7
# OpenStackAgent.py

import shade

class OpenStackAgent(object):

    def __init__(self):
        print("Start init OpenStackClinet object.")

        # Initialize and turn on debug logging
        shade.simple_logging(debug=True)

        # Initialize cloud
        # Cloud configs are read with os-client-config
        cloud = shade.openstack_cloud(cloud='mordred')

    # SHOW
    def show_node(self, para):
        pass

    def show_image(self, para):
        pass

    def show_flavor(self, para):
        pass

    def show_instance(self, para):
        pass

    # ADD
    def add_node(self, para):
        pass

    def add_image(self, para):
        ### TODO
        # Upload an image to the cloud
        # image = cloud.create_image(
        #     'ubuntu-trusty', filename='ubuntu-trusty.qcow2', wait=True)
        image_name = para["image_name"]
        image_file_name = para["image_file_name"]

        image = cloud.create_image(
            image_name, filename=image_file_name, wait=True)

    def add_flavor(self):
        ### TODO
        # Find a flavor with at least 512M of RAM
        # flavor = cloud.get_flavor_by_ram(512)
        pass

    def add_instance(self, image_name, flavor_name):
        # Boot a server, wait for it to boot, and then do whatever is needed
        # to get a public ip for it.
        image = image_name
        flavor = flavor_name
        cloud.create_server(
            'my-server', image=image, flavor=flavor, wait=True, auto_ip=True)

    # DELETE
    def delete_image(self, para):
        pass

    def delete_flavor(self, para):
        pass

    def delete_instance(self, para):
        pass


