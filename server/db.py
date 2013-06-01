# -*- coding: utf-8 -*-
"""
Created on Fri May 31 23:17:31 2013

@author: wy
"""

import sqlite3 as sql
import datetime as dt

class database:
    '''
    数据库操作。
    '''
    def __init__(self):
        self.conn = sql.connect('chat.db')
        self.c = self.conn.cursor()
        
    def insert(self,message,target='dialog'):
        f = message['from']
        t = message['to']
        s = message['sentence']
        time = dt.datetime.now()
        sq='insert into '+target+' values(?,?,?,?)'
        self.c.execute(sq,(f,t,s,time))
        self.conn.commit()
        
    def select(self,order='time',target='dialog'):
        s = 'select * from %s order by %s desc'%(target,order,)
        buf = self.c.execute(s)
        return buf.fetchall()
        
    def close(self):
        self.conn.close()
        
a=database()
b={}
b['from']='haha'
b['to']='hehe'
b['sentence']='hoho'
#a.insert(b)
#print a.c.execute('table').fetchall()
print a.select()
        