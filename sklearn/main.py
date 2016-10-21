from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random

#calculate the Euclidean Distance Between two points
def euclDistance(point1,point2):
    return np.sqrt(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5)
#init points with random
def initPoints(tt,k):
    points=random.sample(tt,k)
    return points
#k-means cluster
def kmeans(tt,k):
    clusterState=True
    clusterAssment=np.zeros([len(tt),2])
   
    points=initPoints(tt,k)
    while clusterState:
        clusterState=False
        for i in range(len(tt)):
            minDist=euclDistance(points[0], tt[i])
            minIndex=0
            for j in range(k):
                distance = euclDistance(points[j],tt[i])
                if distance < minDist:
                    minDist=distance
                    minIndex=j
            #update cluster      
            if clusterAssment[i][0]!=minIndex:
                clusterState=True
                clusterAssment[i][0]=minIndex
                clusterAssment[i][1]=minDist**2
        #calculate the count of each cluster
        #update points
        for j in range(k):
            sumX=0
            countX=0
            sumY=0
            countY=0
            for i in range(len(clusterAssment)):
                if clusterAssment[i][0]==j:
                    sumX+=tt[i][0]
                    countX+=1
                    sumY+=tt[i][1]
                    countY+=1
            try:
                if countX!=0:
                    points[j][0]=sumX/countX
                if countY!=0:
                    points[j][1]=sumY/countY
            except ValueError as err:
                print(err)
    print 'cluster complete...'
    return points,clusterAssment
#show our cluster with different color
def showCluster(tt,k,points,clusterAssment):
    mark = ['or', 'ob', 'og', 'oy', '^r', '+r', 'sr', 'dr', '
    if k > len(mark): 
        print "Sorry! Your k is too disable! please contact donggua" 
        return 1
   
    for i in range(len(clusterAssment)):
        markIndex=int(clusterAssment[i][0])
        plt.plot(tt[i][0],tt[i][1],mark[markIndex])
    mark=['Dr', 'Db', 'Dg', 'Dy', '^b', '+b', 'sb', 'db', '
    for i in range(k): 
        plt.plot(points[i][0], points[i][1], mark[i])
    plt.show()       
