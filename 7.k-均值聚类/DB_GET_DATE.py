#coding:utf-8
import os,re,time,MySQLdb,MySQLdb.cursors,urllib2,random
from redis import Redis
import time
REDIS_HOST = '101.227.79.245'
REDIS_PORT = 16379
PASSWORD="zhengzhouaiwenkejiyouxiangongsidingweitianxiadiyi998"
r=Redis(host=REDIS_HOST, port=REDIS_PORT,password=PASSWORD)


MYSQL_HOST = '171.15.132.56'
MYSQL_DBNAME = 'DataBase_RTB'
MYSQL_USER = 'yanghaochang'
MYSQL_PASSWD = '~Yang6484541'
MYSQL_PORT=33306

conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT)
cur=conn.cursor()

#cur.execute('SELECT latitude,longitude FROM IXDB.Cluster_test;')
cur.execute("SELECT latitude,longitude FROM IXDB.Cluster_test where ip3 = '14.136.111.';")

i = 0
for data in cur.fetchall():
#    print data[0][4:], data[1][5:]
    print data[0], data[1]
    i+=1
