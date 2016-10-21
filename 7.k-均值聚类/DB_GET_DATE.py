#coding:utf-8
import os,re,time,MySQLdb,MySQLdb.cursors,urllib2,random
from redis import Redis
import time


conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT)
cur=conn.cursor()

#cur.execute('SELECT latitude,longitude FROM IXDB.Cluster_test;')
cur.execute("SELECT latitude,longitude FROM IXDB.Cluster_test where ip3 = '14.136.111.';")

i = 0
#print 'begin'
for data in cur.fetchall():
#    print data[0][4:], data[1][5:]
    print data[1], data[0]
    i+=1
