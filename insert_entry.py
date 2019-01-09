#!/usr/bin/python
# -*- coding: utf-8 -*-  
#insert_entry.py
#this module is just for test
import midbox.db.db_services
def insert_entry(type,data):
    db,cursor=db_services.connect_db()
    if type=='image':
        db_services.insert_image(db,cursor,data[0],data[1],data[2],data[3])
    elif type=='host':
        db_services.insert_host(db,cursor,data[0],data[1],data[2],data[3],data[4],data[5],data[6])

if __name__=='__main__':
    type=input()
    if type=='image':
        print('4 paras followed')
        for i in range(0,3):
            data[i]=input()
    elif type=='host':
        print('7 paras followed')
        for i in range(0,6):
            data[i]=input()
