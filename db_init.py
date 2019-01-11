#!/usr/bin/python
# -*- coding: utf-8 -*-
#db_init.py

from midbox._config import MYSQL_USER, MYSQL_PASSWD, MAIN_DB_NAME, DB_SOURCE_SQL, TYPE_DOCKER, TYPE_OPENSTACK

map_images = {
	1:{
		'id':1,
		'func_name':'baseim',
		'local_id':'1',
		'type':TYPE_DOCKER
	},
	2:{
		'id':2,
		'func_name':'docker-snort',
		'local_id':'2',
		'type':TYPE_DOCKER
	},
	3:{
		'id':3,
		'func_name':'vm-iptables',
		'local_id':'05a0d8a2-0489-404d-be1f-e12a92ad3eb3',
		'type':TYPE_OPENSTACK
	},
	4:{
		'id':4,
		'func_name':'vm-tcpdump',
		'local_id':'f9229244-f413-487f-b36e-e734cea6df4f',
		'type':TYPE_OPENSTACK
	},
	5:{
		'id':5,
		'func_name':'vm-snort',
		'local_id':'31c091f5-f090-462c-880c-9ead52df88ee',
		'type':TYPE_OPENSTACK
	}
}


# TODO: 分化处理？
import pexpect
input("This db_init.py will DELETE db_nfv & REcreate it, press ENTER to continue !")

mysql=pexpect.spawn('mysql -u '+MYSQL_USER+' -p')
mysql.sendline(MYSQL_PASSWD)
mysql.sendline('drop database db_nfv;')
mysql.sendline('create database '+MAIN_DB_NAME+';')
create = mysql.expect(['OK','ERROR',])
if create==0:
	mysql.sendline('use '+MAIN_DB_NAME+';')
	mysql.sendline('set names utf8;')
	mysql.sendline('source '+DB_SOURCE_SQL+';')
	imported = mysql.expect(['OK','ERROR',])
	if imported==0:
		mysql.sendline('INSERT INTO t_host (host_id, host_name, ip, pwd, cpu, ram, disk) VALUES (1, "host1", "10.1.1.18", "123456", 8, 32, 100);')
		inserted = mysql.expect(['OK','ERROR',])
		if inserted==1:
			print("insert host failed")

		mysql.sendline('INSERT INTO t_host (host_id, host_name, ip, pwd, cpu, ram, disk) VALUES (2, "host2", "10.1.1.7", "123456", 8, 32, 100);')
		inserted = mysql.expect(['OK','ERROR',])
		if inserted==1:
			print("insert host failed")

		for i in map_images.keys():
			cmd = 'INSERT INTO t_image (image_id, image_local_id, func, type) VALUES ('\
					+ str(map_images[i]['id']) + ', "' + map_images[i]['local_id'] + '", "'\
					+ map_images[i]['func_name'] + '", ' + str(map_images[i]['type']) + ');'
			print(cmd)
			mysql.sendline(cmd)
			inserted = mysql.expect(['OK','ERROR',])
			if inserted==1:
				print("insert image failed")

		# mysql.sendline('INSERT INTO t_image (image_id, image_local_id, func, type) VALUES (2, "2","docker-snort", 1);')
		# inserted = mysql.expect(['OK','ERROR',])
		# if inserted==1:
		# 	print("insert image failed")

		# mysql.sendline('INSERT INTO t_image (image_id, image_local_id, func, type) VALUES (3, "2","vm-iptables", 2);')
		# inserted = mysql.expect(['OK','ERROR',])
		# if inserted==1:
		# 	print("insert image failed")

		# mysql.sendline('INSERT INTO t_image (image_id, image_local_id, func, type) VALUES (4, "2","vm-tcpdump", 2);')
		# inserted = mysql.expect(['OK','ERROR',])
		# if inserted==1:
		# 	print("insert image failed")

		# mysql.sendline('INSERT INTO t_image (image_id, image_local_id, func, type) VALUES (5, "2","vm-snort", 2);')
		# inserted = mysql.expect(['OK','ERROR',])
		# if inserted==1:
		# 	print("insert image failed")

		mysql.sendline('exit')
	elif imported==1:
		print("import database failed")
		mysql.sendline('exit')
elif create==1:
	print("create database failed")
	mysql.sendline('exit')
