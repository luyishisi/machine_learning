#coding:utf-8
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from itertools import cycle
import sys
import csv
import os,re,time,MySQLdb,MySQLdb.cursors,urllib2,random



try:
    conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
    cur = conn.cursor()
    print "mysql connect beging"
except Exception,e:
		print Exception,e

def get_ll(ip3,conn,cur):
    print ip3
    mysql_str = '''SELECT latitude,longitude FROM DataBase_RTB.Sorted_test_copy where ip3 = '%s' ;'''
    mysql_str =  mysql_str %(ip3)
    try:
    	conn.ping()
    except Exception,e:
    	print Exception,e
    	conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
    	cur = conn.cursor()
    try:
        cur.execute(mysql_str)
        dataSet = []
        for data in cur.fetchall():
            dataSet.append([float(data[1]), float(data[0])])
        #print dataSet
        return dataSet
    except Exception,e:
		print Exception,e
    return 1


def insert_ll(address_ll,conn,cur):
    mysql_str = '''update DataBase_RTB.Sorted_test_copy set center_ll = %s ,group_id = %s  where ip3 = %s and  latitude = %s and longitude = %s'''
    try:
    	conn.ping()
    except Exception,e:
    	print Exception,e
    	conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
    	cur = conn.cursor()
    try:
        cur.execute(mysql_str,address_ll)
        conn.commit()
    except Exception,e:
		print Exception,e
    return None

def get_ip3(conn,cur):
    mysql_str = '''select ip3 from DataBase_RTB.Sorted_test_copy  group by ip3;'''
    try:
    	conn.ping()
    except Exception,e:
    	print Exception,e
    	conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
    	cur = conn.cursor()
    try:
        cur.execute(mysql_str)
        dataip3 = []
        for data in cur.fetchall():
            dataip3.append(data[0])
        return dataip3
    except Exception,e:
		print Exception,e
    return 1

ip3_3 = get_ip3(conn,cur)

num = 0
while(num <= 19661):
    print '*******************************8',num,time.ctime()

    # 载入数据集合
    ip3_up = (ip3_3[num])
    #ip3_up = ('1.36.'+str(ip3_3)+'.')

    dataSet = get_ll(ip3_up,conn,cur)
    #print dataSet
    if(dataSet == 1):
        print 'get_ll error time.sleep 100',time.ctime()
        time.sleep(10)
    X = np.array(dataSet) #list to array

    # MeanShift 计算
    try:
        bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True,cluster_all=True).fit(X)
    except Exception,e:
        num += 1
        print num ,"&&&&&&&&&&&&&&&&&&&&&&&",time.ctime()
        print Exception,e
        continue

    arr_flag = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in ms.labels_:
        arr_flag[i]+=1
    #print  arr_flag
    k = 0
    for i in arr_flag:
        if(i > 3):
            k +=1
    print k

    numSamples = len(dataSet)
    cluster_centers = ms.cluster_centers_

    for ki in xrange(5):
        for i in xrange(numSamples):
        #for j in xrange(numSamples):
            if(ms.labels_[i] == ki):
                #print ms.labels_[i],dataSet[i][0],dataSet[i][1],cluster_centers[ki][0],cluster_centers[ki][1]

                center_ll = str(cluster_centers[ki][0])+','+str(cluster_centers[ki][1])
                group_id = ms.labels_[i]
                #latitude = str(dataSet[i][1])
                #longitude = str(dataSet[i][0])
                latitude = "%0.6f" %(dataSet[i][1])
                longitude = "%0.6f" %(dataSet[i][0])
                ip3 = ip3_up
                address_ll = (center_ll,group_id,ip3,latitude,longitude)
                #print address_ll
                insert_ll(address_ll,conn,cur)
                #update DataBase_RTB.Sorted_test_copy set center_ll = %s ,group_id = %s  where ip3 = %s and  latitude = %s and longitude = %s
    #ip3_3 += 1
    num += 1

    print 'time.sleep',ip3_up,num




    '''
    labels = ms.labels_
    print labels
    cluster_centers = ms.cluster_centers_
    print cluster_centers

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    plt.figure(1)
    plt.clf()
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)

    plt.xlim(113.848277, 114.382373)
    plt.ylim(22.175509, 22.529357)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    '''
    time.sleep(0)





'''
clf = KMeans(n_clusters=k, random_state=0).fit(X)

mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
#画出所有样例点 属于同一分类的绘制同样的颜色
print '************8888'
for i in xrange(numSamples):
    plt.plot(dataSet[i][0], dataSet[i][1], mark[clf.labels_[i]]) #mark[markIndex])
    if(clf.labels_[i] == 1):
        pass
        #print "%0.6f %0.6f" %(dataSet[i][0]*(114.382373-113.848277)+113.848277 ,dataSet[i][1]*(22.529357-22.175509)+22.175509)
        #print clf.labels_[i],dataSet[i][0],dataSet[i][1]
    # 画出质点，用特殊图型
print '************8888'

mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
centroids =  clf.cluster_centers_
print centroids
for i in range(k):
    plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize = 12)
    #print "%0.6f %0.6f" %(centroids[i, 0]*(114.382373-113.848277)+113.848277 ,centroids[i, 1]*(22.529357-22.175509)+22.175509)

print clf.inertia_
plt.xlim(113.848277, 114.382373)
plt.ylim(22.175509, 22.529357)
#plt.xlim(0, 1)
#plt.ylim(0, 1)

plt.show()

print '***************************************'
labels = ms.labels_
print labels
cluster_centers = ms.cluster_centers_
print cluster_centers

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')

for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)

plt.xlim(113.848277, 114.382373)
plt.ylim(22.175509, 22.529357)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
'''
