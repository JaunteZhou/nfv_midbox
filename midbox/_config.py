#!/usr/bin/python
# -*- coding: utf-8 -*-
#_config.py

##### docker registry config #####
DOCKER_REGISTRY_IP = '10.1.1.7'
DOCKER_REGISTRY_PORT = '5001'
DOCKER_REGISTRY_WORK_DIRECTORY = '/home/nfv30/registry'
##### docker registry config end #####

##### physical port name config #####
# physical port name should be the same on every host
IN_PORT   ='eno3'
OUT_PORT  ='eno3'

DATA_PLANE_OVS_NAME = 'sw1'
##### physical port name config end #####

##### log config #####
debug_rotating_log_filename = 'all.log'
error_log_filename          = 'error.log'
base_dir                    = 'logs'
debug_rotating_log_dir      = base_dir + '/' + debug_rotating_log_filename
error_log_dir               = base_dir + '/' + error_log_filename
##### log config end #####



##### db config ######
MYSQL_IP_ADDR   = 'localhost'
MYSQL_USER      = 'root'
MYSQL_PASSWD    = 'openstack'
MAIN_DB_NAME    = 'db_nfv'
DB_SOURCE_SQL   = '/home/nfv30/nfv_midbox/midbox/db/nfvlab.sql'
##### db config end #####



##### midbox config #####
TYPE_DOCKER     = 1
TYPE_OPENSTACK  = 2
##### midbox config end #####



##### openstack config #####
SERVERS_NAME_PREFIX = "S"
FLAVORS_ID_PREFIX   = "F"
IMAGE_NAME_PREFIX   = "I"
# user info
user_name           = "admin"
user_id             = "c7f6506acf8a4204b07cc412f426d2b3"
password            = "openstack"
# project info, tenant is the same as project
tenant_name         = "admin"  
tenant_id           = "b4b90ce3692c4592af6ccb40ac1f0785"

# openstack server ip
service_ip          = "10.1.1.18"

# service restful api url
service_base_url 	= "http://" + service_ip
block_url 			= service_base_url + "/volume/v3/" + tenant_id
compute_url 		= service_base_url + "/compute/v2.1"
compute_legacy_url 	= service_base_url + "/compute/v2/" + tenant_id
identity_url 		= service_base_url + "/identity"
image_url 			= service_base_url + "/image/v2"
networking_url 		= service_base_url + ":9696/v2.0"
placement_url 		= service_base_url + "/placement"
volume_url 			= service_base_url + "/volume/v1/" + tenant_id
volumev2_url 		= service_base_url + "/volume/v2/" + tenant_id
volumev3_url 		= service_base_url + "/volume/v3/" + tenant_id

auth_token_url      = identity_url + "/v3/auth/tokens"
volumes_url         = volumev3_url + "/volumes"
servers_url         = compute_url + "/servers"
flavor_url          = compute_url + "/flavors"
hypervisors_url     = compute_url + "/os-hypervisors"
simple_usage_url    = compute_url + "/os-simple-tenant-usage"
images_url          = image_url + "/images"
networks_url        = networking_url + "/networks"
floating_url        = networking_url + "/floatingips"
ports_url           = networking_url + "/ports"

# networks name and id
#public_net_id       = "d27d54f3-f89c-41e5-a973-4e449a34a2a6"
#public_net_name     = "public-net"
data_in_net_id      = "46355ffe-3c0c-4041-b6d3-3f73a696085f"
data_in_net_name    = "data-in-net"
data_out_net_id     = "e2b132f2-7f29-4bd6-b526-1c497fda6be7"
data_out_net_name   = "data-out-net"
private_net_id      = "47027190-71bb-49a3-a585-1f330531216f"
private_net_name    = "private-net"

# sleep time in attaching
SLEEP_SECONDS_IN_WAITING = 1
SLEEP_SECONDS_IN_ATTACHING = 2
##### openstack config end #####