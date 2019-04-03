#!/usr/bin/python
# -*- coding: utf-8 -*-
# db_init.py

from midbox._config import MYSQL_USER, MYSQL_PASSWD, MAIN_DB_NAME, DB_SOURCE_SQL, TYPE_DOCKER, TYPE_OPENSTACK
import pexpect

# map_images = {
#     1: {
#         'image_id': 1,
#         'func': 'baseim',
#         'image_local_id': '1',
#         'type': TYPE_DOCKER
#     },
#     2: {
#         'image_id': 2,
#         'func': 'docker-snort',
#         'image_local_id': '2',
#         'type': TYPE_DOCKER
#     },
#     3: {
#         'image_id': 3,
#         'func': 'vm-iptables',
#         'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
#         'type': TYPE_OPENSTACK
#     },
#     4: {
#         'image_id': 4,
#         'func': 'vm-tcpdump',
#         'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
#         'type': TYPE_OPENSTACK
#     },
#     5: {
#         'image_id': 5,
#         'func': 'vm-snort',
#         'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
#         'type': TYPE_OPENSTACK
#     }
# }

DB_ITEM_DICT = {
    't_host': [
        {
            'host_id': 1,
            'host_name': "host1",
            'ip': "10.1.1.18",
            'pwd': "123456",
            'cpu': 8,
            'ram': 32,
            'disk': 100
        },
        {
            'host_id': 2,
            'host_name': "host2",
            'ip': "10.1.1.7",
            'pwd': "123456",
            'cpu': 8,
            'ram': 32,
            'disk': 100
        }
    ],
    't_image': [
        {
            'image_id': 1,
            'func': 'baseim',
            'image_local_id': '1',
            'type': TYPE_DOCKER
        },
        {
            'image_id': 2,
            'func': 'docker-snort',
            'image_local_id': '2',
            'type': TYPE_DOCKER
        },
        {
            'image_id': 3,
            'func': 'vm-iptables',
            'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
            'type': TYPE_OPENSTACK
        },
        {
            'image_id': 4,
            'func': 'vm-tcpdump',
            'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
            'type': TYPE_OPENSTACK
        },
        {
            'image_id': 5,
            'func': 'vm-snort',
            'image_local_id': '3ba86015-8b57-4a2c-ab7d-105a7f4e9fe2',
            'type': TYPE_OPENSTACK
        }
    ]
}


def __edit_cmd_of_insert_to_db(item_dic):
    cmd = 'INSERT INTO ' + table_name + ' ('
    for item_name in item_dic:
        cmd += item_name + ','
    cmd = cmd[:-1]
    cmd += ') VALUES ('
    for item_name in item_dic:
        if type(item_dic[item_name]) is str:
            cmd += '"' + item_dic[item_name] + '",'
        else:
            cmd += item_dic[item_name] + ','
    cmd = cmd[:-1]
    cmd += ');'
    return cmd


if __name__ == "__main__":
    raw_input("This db_init.py will DELETE db_nfv & REcreate it, press ENTER to continue !")

    mysql = pexpect.spawn('mysql -u ' + MYSQL_USER + ' -p')
    mysql.sendline(MYSQL_PASSWD)
    mysql.sendline('drop database db_nfv;')
    delete = mysql.expect(['OK', 'ERROR', ])
    if delete == 1:
        print('db_nfv donnot exist.')
    mysql.sendline('create database ' + MAIN_DB_NAME + ';')
    create = mysql.expect(['OK', 'ERROR', ])
    if create == 0:
        mysql.sendline('use ' + MAIN_DB_NAME + ';')
        mysql.sendline('set names utf8;')
        mysql.sendline('source ' + DB_SOURCE_SQL + ';')
        imported = mysql.expect(['OK', 'ERROR', ])
        if imported == 0:
            # mysql.sendline(
            #     'INSERT INTO t_host (host_id, host_name, ip, pwd, cpu, ram, disk) VALUES (1, "host1", "10.1.1.18", "123456", 8, 32, 100);')
            # inserted = mysql.expect(['OK', 'ERROR', ])
            # if inserted == 1:
            #     print("insert host failed")
            #
            # mysql.sendline(
            #     'INSERT INTO t_host (host_id, host_name, ip, pwd, cpu, ram, disk) VALUES (2, "host2", "10.1.1.7", "123456", 8, 32, 100);')
            # inserted = mysql.expect(['OK', 'ERROR', ])
            # if inserted == 1:
            #     print("insert host failed")

            for table_name in DB_ITEM_DICT:
                for item_dic in DB_ITEM_DICT[table_name]:
                    cmd = __edit_cmd_of_insert_to_db(item_dic)
                    print(cmd)
                    mysql.sendline(cmd)
                    inserted = mysql.expect(['OK', 'ERROR', ])
                    if inserted == 1:
                        print("insert " + table_name + " failed")

            # for i in map_images.keys():
            #     cmd = 'INSERT INTO t_image (image_id, image_local_id, func, type) VALUES (' + \
            #           str(DB_ITEM_DICT['t_image'][i]['image_id']) + ', ' + \
            #           '"' + DB_ITEM_DICT['t_image'][i]['image_local_id'] + '", ' + \
            #           '"' + DB_ITEM_DICT['t_image'][i]['func'] + '", ' + \
            #           str(DB_ITEM_DICT['t_image'][i]['type']) + ');'
            #     print(cmd)
            #     mysql.sendline(cmd)
            #     inserted = mysql.expect(['OK', 'ERROR', ])
            #     if inserted == 1:
            #         print("insert image failed")

            mysql.sendline('exit')
        elif imported == 1:
            print("import database failed")
            mysql.sendline('exit')
    elif create == 1:
        print("create database failed")
        mysql.sendline('exit')
