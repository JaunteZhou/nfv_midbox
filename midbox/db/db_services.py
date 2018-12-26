#!/usr/bin/python
# -*- coding: utf-8 -*-  
#db_services.py

import pymysql  
import types

from midbox.db.mysql_config import MYSQL_IP_ADDR, MYSQL_USER, MYSQL_PASSWD, MAIN_DB_NAME

def connect_db(): 
	db=pymysql.connect(MYSQL_IP_ADDR, MYSQL_USER, MYSQL_PASSWD, MAIN_DB_NAME)
  
	cursor=db.cursor()  
	return db, cursor
	
def close_db(db, cursor):
	# 关闭数据库连接
	cursor.close()
	db.close()

m_table_key = {
	"t_function": "fe_id",
	"t_image": "image_id",
	"t_host": "host_id",
	"t_flow": "flow_id",
}

def executeSql(db, cursor, sql):
	try:
		cursor.execute(sql)
		db.commit()
		return 1
	except Exception as e:
		print(e)
		db.rollback()
		return 0

#添加数据
def insert_function(db, cursor, fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, disk, ref_count):
	fe_id=int(fe_id)
	image_id=int(image_id)
	host_id=int(host_id)
	func_local_id=str(func_local_id)
	ip=str(ip)
	pwd=str(pwd)
	cpu=int(cpu)
	ram=int(ram)
	type=int(type)
	disk=int(disk)
	ref_count=int(ref_count)
	#插入数据  
	sql="INSERT INTO t_function (fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, disk, ref_count) VALUES \
	('%d', '%d', '%d', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d')" % \
	(fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, disk, ref_count)

	return executeSql(db, cursor, sql)
	
		
def insert_image(db, cursor, image_id, image_local_id, func, type):
	
	image_id=int(image_id)
	image_local_id=str(image_local_id)
	type=int(type)
	func=str(func)
	#插入数据  
	sql="INSERT INTO t_image (image_id, image_local_id, func, type) VALUES \
	('%d', '%s', '%s', '%d')" % \
	(image_id, image_local_id, func, type)	

	return executeSql(db, cursor, sql)

		
def insert_host(db, cursor, host_id, host_name, ip, pwd, cpu, ram, disk):
	host_id=int(host_id)
	host_name=str(host_name)
	ip=str(ip)
	pwd=str(pwd)
	cpu=int(cpu)
	ram=int(ram)
	disk=int(disk)
	#插入数据  
	sql="INSERT INTO t_host (host_id, host_name, ip, pwd, cpu, ram, disk) VALUES \
	('%d', '%s', '%s', '%s', '%d', '%d', '%d')" % \
	(host_id, host_name, ip, pwd, cpu, ram, disk)	

	return executeSql(db, cursor, sql)
		
		
def insert_flow(db, cursor, flow_id, chain, match_field):
	flow_id=int(flow_id)
	chain=str(chain)
	match_field=str(match_field)
	#插入数据  
	sql="INSERT INTO t_flow (flow_id, chain, match_field) VALUES \
	('%d', '%s', '%s')" % \
	(flow_id, chain, match_field)	

	return executeSql(db, cursor, sql)

	

#更新数据		
def update_table(db, cursor, table, condition, value, id):
	#更新 
	if isinstance(value, (int)):
		a=str(value)
	else:
		a="'"+value+"'"

	sql="update " + table + " set " + condition + "=" + a + " where " + m_table_key[table] + "=" + str(id)
	return executeSql(db, cursor, sql)
			

#删除数据		
def delete_table(db, cursor, table, id):
	
	sql="delete from " + table + " where " + m_table_key[table] + "=" + str(id)
	return executeSql(db, cursor, sql)

m_table_items = {
	"t_function": ["fe_id","image_id","host_id","func_local_id","ip","pwd","cpu","ram","type","disk","ref_count"],
	"t_image": ["image_id","image_local_id","func","type"],
	"t_host": ["host_id","host_name","ip","pwd","cpu","ram","disk"],
	"t_flow": ["flow_id","chain","match_field"],
}

#查询数据			
def show_table(db, cursor, table):
	#查询 
	sql="select * from "+table
	cursor.execute(sql)  
  
	results=cursor.fetchall()  
	
	line = ""
	for item in m_table_items[table]:
		line += item + "\t"
	print (line)
	if results!=():
		for each in results:
			line = ""
			for each_item in each:
				if isinstance(each_item, (int)):
					a=str(each_item)
				else:
					a=each_item
				line += a + "\t"
			print (line)

			
def select_table(db, cursor, table, attribute, id):
	#查询 
	
	sql="select " + attribute + " from "+ table +" where " + m_table_key[table] + "=" + str(id)

	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	if not results:
		return results
	else:
		return results[0][0]
	
	
def select_function(db, cursor, host_id):
	sql="select fe_id from t_function where host_id=" + str(host_id)

	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	list=[]
	if not results:
		return results
	else:
		
		for each in results:
			list.append(each[0])
		return list
		
def select_condition(db, cursor, table, attribute, condition, value):
	if isinstance(value, (int)):
		a=str(value)
	else:
		a=value
	sql="select " + attribute + " from " + table + " where " + condition + "=" + a
	
	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	list=[]
	if not results:
		return results
	else:
		
		for each in results:
			list.append(each[0])
		return list
		
def select_id(db, cursor, table):
	sql="select " + m_table_key[table] + " from " + table
	
	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	list=[]
	if not results:
		return results
	else:
		for each in results:
			list.append(each[0])
		return list
	
if __name__ == "__main__":
	db, cursor = connect_db()
	#show_table(db, cursor, "t_image")
	#print(select_table(db, cursor, "t_host", "ip", 2))
	#print(update_table(db, cursor, "t_host", "cpu", 2, 3))
	#print(delete_table(db, cursor, "t_image", 1))
	#print(insert_image(db, cursor, "1", "192.168.1.3", "1"))
	#print(select_condition(db, cursor, "t_host", "ip", "cpu", 2))
	#select_condition(db, cursor, "t_host", "host_id", "cpu", 2)
	#print(select_id(db, cursor, "t_host"))
	close_db(db, cursor)