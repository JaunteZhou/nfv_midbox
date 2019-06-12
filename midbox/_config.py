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
TRY_NUM = 60
SLEEP_TIME_OF_TRY = 5

# physical port name config
# 当前设计中，每个服务器的物理端口名称必须相同
IN_PORT = 'eno3'
OUT_PORT = 'eno3'

# virtual switch name config
# 虚拟交换机名的配置
DATA_PLANE_SW_NAME = 'sw1'
CTRL_PLANE_SW_NAME = 'sw-man'
OPENSTACK_SW_NAME = 'br-int'
OPENSTACK_PORT_NAME_HEAD = "qvo"

# db config
# 数据库配置
MYSQL_IP_ADDR   = 'localhost'
MYSQL_USER      = 'root'
MYSQL_PASSWD    = '123456'
MAIN_DB_NAME    = 'db_nfv'
DB_SOURCE_SQL   = '/home/nfv30/nfv_midbox/midbox/db/nfvlab.sql'

# midbox config
# 中间件自身配置
TYPE_DOCKER = 1
TYPE_OPENSTACK = 2
STR_TYPE_TO_NUM_TYPE = {
    "vm": TYPE_OPENSTACK,
    "container": TYPE_DOCKER
}

# docker registry config
DOCKER_REGISTRY_IP = '10.0.30.10'
DOCKER_REGISTRY_PORT = '5001'
DOCKER_REGISTRY_WORK_DIRECTORY = '/home/nfv30/registry'
DOCKER_SERVICE_FILE_PATH = '/usr/lib/systemd/system/docker.service'

# openstack config
SERVERS_NAME_PREFIX = "S"
FLAVORS_ID_PREFIX = "F"
IMAGE_NAME_PREFIX = "I"
# openstack用户信息
USER_NAME = "admin"
USER_ID = "93659fafc3ed45328a3fc37b53bf6bc8"
USER_PWD = "32576992ba2c4e13"
# openstack项目（租户）信息
PROJECT_NAME = "admin"
PROJECT_ID = "77bff281e27c4f87ba07d65c984cdbe4"

# openstack控制节点服务器IP地址
service_ip = "10.0.30.51"
# openstack service restful api url
# openstack相关基础服务的RESTful API URL
service_base_url 	= "http://" + service_ip
block_url 			= service_base_url + ":8776/v3/" + PROJECT_ID
compute_url 		= service_base_url + ":8774/v2.1"
compute_legacy_url 	= service_base_url + ":8774/v2/" + PROJECT_ID
identity_url 		= service_base_url + ":5000"
image_url 			= service_base_url + ":9292/v2"
networking_url 		= service_base_url + ":9696/v2.0"
placement_url 		= service_base_url + ":8778/placement"
volume_url 			= service_base_url + ":8776/v1/" + PROJECT_ID
volumev2_url 		= service_base_url + ":8776/v2/" + PROJECT_ID
volumev3_url 		= service_base_url + ":8776/v3/" + PROJECT_ID
# openstack相关具体服务RESTful API URL
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

# openstack中networks名称与ID
private_net_id      = "1467b2c5-d976-49b1-858b-786ac788f236"
private_net_name    = "private-net"
data_in_net_id      = "7372f98d-79e5-4cef-9711-7a50f299fb99"
data_in_net_name    = "data-in-net"
data_out_net_id     = "88209712-b7b1-4df4-ba08-78dd346f9bb0"
data_out_net_name   = "data-out-net"
