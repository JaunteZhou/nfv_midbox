#!/usr/bin/python3
# -*- coding: utf-8 -*-
#openstack_config.py
import os

# user info
user_name = "admin"
user_id = "fddd028756464ddd853d66bb93eb5e60"
password = "openstack"
# project info, tenant is the same as project
tenant_name = "admin"  
tenant_id = "e922a17e84cc4b8e83a9ea441a650c0e"
#src_port_list = ["8591fa39-3fdb-40d5-b80c-928f90325598", "6122ff78-0533-4e7a-a203-61fb0c4fabcd", "0f636ebe-2630-4f9e-a2df-f7a961f80514"]
#dst_ip = "10.0.0.47/32"

# openstack server ip
service_ip = "10.1.1.18"

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
flavor_url          = compute_url + "/flavors"
networks_url        = networking_url + "/networks"
floating_url        = networking_url + "/floatingips"
ports_url           = networking_url + "/ports"
simple_usage_url    = compute_url + "/os-simple-tenant-usage"
# abs_root_dir
abs_root_dir = "/Users/JaunteZhou/Documents/NFV30py"
abs_auth_json_dir = abs_root_dir + "/nfv30py/southbound/ostk_rest_api/auth.json"

public_net_id = "d27d54f3-f89c-41e5-a973-4e449a34a2a6"
public_net_name = "public-net"
data_flow_net_id = "8053a2a5-18c2-4c47-a525-9d0c687660f9"
data_flow_net_name = "data-flow-net"
private_net_id = "5aa80307-7a0a-48ec-ad2a-a2fc10be3eb7"
private_net_name = "private-net"