#!/usr/bin/python
# -*- coding: utf-8 -*-  
# unused_insert_entry.py
# this module is just for test
from midbox.db import db_services


def insert_entry(data_type, data):
    db, cursor = db_services.connect_db()
    if data_type == 'image':
        db_services.insert_image(db, cursor, data[0], data[1], data[2], data[3])
    elif data_type == 'host':
        db_services.insert_host(db, cursor, data[0], data[1], data[2], data[3], data[4], data[5], data[6])


if __name__ == '__main__':
    data_type = input()
    data = []
    if data_type == 'image':
        print('4 paras followed')
        for i in range(0, 3):
            data.append(input())
    elif data_type == 'host':
        print('7 paras followed')
        for i in range(0, 6):
            data.append(input())
