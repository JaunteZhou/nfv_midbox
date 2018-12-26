#!/usr/bin/python
# -*- coding: utf-8 -*-
#_config.py

# test config
config1 = 1
config2 = "2"
config3 = [3,3,3]
# ignore


##### log config #####
debug_rotating_log_filename = 'all.log'
error_log_filename          = 'error.log'
base_dir                    = 'log'
debug_rotating_log_dir      = base_dir + '/' + debug_rotating_log_filename
error_log_dir               = base_dir + '/' + error_log_filename
##### log config end #####



##### db config ######
MYSQL_IP_ADDR   = 'localhost'
MYSQL_USER      = 'root'
MYSQL_PASSWD    = '123456'
MAIN_DB_NAME    = 'db_nfv'
##### db config end #####



##### midbox config #####
TYPE_DOCKER     = 1
TYPE_OPENSTACK  = 2
##### midbox config end #####



##### openstack config #####
# user info
user_name           = "admin"
user_id             = "fddd028756464ddd853d66bb93eb5e60"
password            = "openstack"
# project info, tenant is the same as project
tenant_name         = "admin"  
tenant_id           = "e922a17e84cc4b8e83a9ea441a650c0e"

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
public_net_id       = "d27d54f3-f89c-41e5-a973-4e449a34a2a6"
public_net_name     = "public-net"
data_flow_net_id    = "8053a2a5-18c2-4c47-a525-9d0c687660f9"
data_flow_net_name  = "data-flow-net"
private_net_id      = "5aa80307-7a0a-48ec-ad2a-a2fc10be3eb7"
private_net_name    = "private-net"

# sleep time in attaching
SLEEP_SECONDS_IN_ATTACHING = 2
##### openstack config end #####