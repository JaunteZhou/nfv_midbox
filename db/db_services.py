#!/usr/bin/python3  
import pymysql  
import types  
 
def connect_db(): 
	db=pymysql.connect("localhost","root","123456","db_nfv")

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
def insert_function(db, cursor,fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, size, ref_count):
	#插入数据  
	sql = "INSERT INTO t_function \
	(fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, size, ref_count) VALUES \
	('%d', '%d', '%d', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d')" % \
	(fe_id, image_id, host_id, func_local_id, ip, pwd, cpu, ram, type, size, ref_count)

	return executeSql(db, cursor, sql)
	
		
def insert_image(db, cursor, image_id, func, type):
	
	#插入数据  
	sql="INSERT INTO t_image (image_id, func, type) VALUES \
	('%d', '%s', '%d')" % \
	(image_id, func, type)	

	return executeSql(db, cursor, sql)

		
def insert_host(db, cursor, host_id, ip, pwd, cpu, ram, disk):
	#插入数据  
	sql="INSERT INTO t_host (host_id, ip, pwd, cpu, ram, disk) VALUES \
	('%d', '%s', '%s', '%d', '%d', '%d')" % \
	(host_id, ip, pwd, cpu, ram, disk)	

	return executeSql(db, cursor, sql)
		
		
def insert_flow(db, cursor, flow_id, chain, match_field):
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
	"t_function": ["fe_id","image_id","host_id","func_local_id","ip","pwd","cpu","ram","type","size","ref_count"],
	"t_image": ["image_id","func","type"],
	"t_host": ["host_id","ip","pwd","cpu","ram","disk"],
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
	
	return results[0][0]	
	
	
def select_function(db, cursor, host_id):
	sql="select fe_id from t_function where host_id=" + str(host_id)

	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	list=[]
	
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
	
	for each in results:
		list.append(each[0])
	return list

def select_id(db, cursor, table):
	sql="select " + m_table_key[table] + " from " + table
	
	cursor.execute(sql)  
	results=cursor.fetchall()  
	
	list=[]
	
	for each in results:
		list.append(each[0])
	return list
	
	
if __name__ == "__main__":
	db, cursor = connect_db()
	show_table(db, cursor, "t_flavor")
	#print(select_table(db, cursor, "t_host", "ip", 2))
	#print(update_table(db, cursor, "t_host", "cpu", 2, 3))
	#print(delete_table(db, cursor, "t_host", 1))
	#print(insert_host(db, cursor, 1, "192.168.1.3", "112211", 4, 64, 64))
	#print(select_condition(db, cursor, "t_host", "ip", "cpu", 2))
	#select_condition(db, cursor, "t_host", "host_id", "cpu", 2)
	#print(select_id(db, cursor, "t_host"))
	close_db(db, cursor)