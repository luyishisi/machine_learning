#coding:utf-8
import os,re,time,MySQLdb,MySQLdb.cursors,urllib2,random
from redis import Redis
import time


conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT)
cur=conn.cursor()

cur.execute("SELECT  latitude,longitude FROM DataBase_RTB.Sorted_test_10w where ip3 = '1.36.0.' ;")
#cur.execute("SELECT latitude,longitude FROM IXDB.Cluster_test where ip3 = '14.136.164.';")

i = 0
for data in cur.fetchall():
#    print data[0][4:], data[1][5:]
    print data[1],data[0]
    #print (float(data[1])-113.848277)/(114.382373-113.848277), (float(data[0])-22.175509)/(22.529357-22.175509)
    i+=1
