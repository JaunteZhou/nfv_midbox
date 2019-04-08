#!/usr/bin/python
# -*- coding: utf-8 -*-
# _config.py

# log config
debug_rotating_log_filename = 'all.log'
error_log_filename = 'error.log'
base_dir = 'logs'
debug_rotating_log_dir = base_dir + '/' + debug_rotating_log_filename
error_log_dir = base_dir + '/' + error_log_filename

# sleep time
# 睡眠时间大小
SLEEP_SECONDS_IN_WAITING = 2
SLEEP_SECONDS_IN_ATTACHING = 2

# physical port name config
# 当前设计中，每个服务器的物理端口名称必须相同
IN_PORT = 'eno3'
OUT_PORT = 'eno3'

# virtual switch name config
# 虚拟交换机名的配置
DATA_PLANE_SW_NAME = 'sw1'
CTRL_PLANE_SW_NAME = 'sw-man'
OPENSTACK_SW_NAME = 'br-int'

# db config
# 数据库配置
MYSQL_IP_ADDR = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'openstack'
MAIN_DB_NAME = 'db_nfv'
DB_SOURCE_SQL = '/home/nfv30/nfv_midbox/midbox/db/nfvlab.sql'

# midbox config
# 中间件自身配置
TYPE_DOCKER = 1
TYPE_OPENSTACK = 2
STR_TYPE_TO_NUM_TYPE = {
    "vm": TYPE_OPENSTACK,
    "container": TYPE_DOCKER
}

# docker registry config
DOCKER_REGISTRY_IP = '10.1.1.7'
DOCKER_REGISTRY_PORT = '5001'
DOCKER_REGISTRY_WORK_DIRECTORY = '/home/nfv30/registry'

# openstack config
SERVERS_NAME_PREFIX = "S"
FLAVORS_ID_PREFIX = "F"
IMAGE_NAME_PREFIX = "I"
# openstack用户信息
USER_NAME = "admin"
USER_ID = "c7f6506acf8a4204b07cc412f426d2b3"
USER_PWD = "openstack"
# openstack项目（租户）信息
TENANT_NAME = "admin"
TENANT_ID = "b4b90ce3692c4592af6ccb40ac1f0785"
# openstack控制节点服务器IP地址
service_ip = "10.1.1.18"
# openstack service restful api url
# openstack相关基础服务的RESTful API URL
service_base_url = "http://" + service_ip
block_url = service_base_url + "/volume/v3/" + TENANT_ID
compute_url = service_base_url + "/compute/v2.1"
compute_legacy_url = service_base_url + "/compute/v2/" + TENANT_ID
identity_url = service_base_url + "/identity"
image_url = service_base_url + "/image/v2"
networking_url = service_base_url + ":9696/v2.0"
placement_url = service_base_url + "/placement"
volume_url = service_base_url + "/volume/v1/" + TENANT_ID
volumev2_url = service_base_url + "/volume/v2/" + TENANT_ID
volumev3_url = service_base_url + "/volume/v3/" + TENANT_ID
# openstack相关具体服务RESTful API URL
auth_token_url = identity_url + "/v3/auth/tokens"
volumes_url = volumev3_url + "/volumes"
servers_url = compute_url + "/servers"
flavor_url = compute_url + "/flavors"
hypervisors_url = compute_url + "/os-hypervisors"
simple_usage_url = compute_url + "/os-simple-tenant-usage"
images_url = image_url + "/images"
networks_url = networking_url + "/networks"
floating_url = networking_url + "/floatingips"
ports_url = networking_url + "/ports"
# openstack中networks名称与ID
data_in_net_id = "46355ffe-3c0c-4041-b6d3-3f73a696085f"
data_in_net_name = "data-in-net"
data_out_net_id = "e2b132f2-7f29-4bd6-b526-1c497fda6be7"
data_out_net_name = "data-out-net"
private_net_id = "47027190-71bb-49a3-a585-1f330531216f"
private_net_name = "private-net"
