#!/usr/bin/python
# -*- coding: utf-8 -*-
#Initialize.py

# TODO: 分化处理？
import pexpect
mysql=pexpect.spawn('mysql -u root -p')
mysql.sendline('123456')
mysql.sendline('create database db_nfv;')
create = mysql.expect(['OK','ERROR',])
if create==0:
	mysql.sendline('use db_nfv;')
	mysql.sendline('set names utf8;')
	mysql.sendline('source /home/nfv30/nfv_midbox/db/nfvlab.sql;')
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
		mysql.sendline('INSERT INTO t_image (image_id, image_local_id, func, type, ) VALUES (1, "123","bimage", 1);')
		inserted = mysql.expect(['OK','ERROR',])
		if inserted==1:
			print("insert host failed")
		mysql.sendline('exit')
		
	elif imported==1:
		print("import database failed")
		mysql.sendline('exit')
elif create==1:
	print("create database failed")
	mysql.sendline('exit')
