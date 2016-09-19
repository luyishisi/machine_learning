#coding=utf-8
from numpy import *
import operator

def createDataSet():
    group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
    labels = ['C','C','A','A']
    #print group,labels
    return group,labels
#inputX表示输入向量（也就是我们要判断它属于哪一类的）
#dataSet表示训练样本
#label表示训练样本的标签
#k是最近邻的参数，选最近k个
def kNNclassify(inputX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]#计算有几个训练数据
    #开始计算欧几里得距离
    diffMat = tile(inputX, (dataSetSize,1)) - dataSet
    
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)#矩阵每一行向量相加
    distances = sqDistances ** 0.5
    #欧几里得距离计算完毕
    sortedDistance = distances.argsort()
    classCount = {}
    for i in xrange(k):
        voteLabel = labels[sortedDistance[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
    res = max(classCount)
    return res

def main():
    group,labels = createDataSet()
    t = kNNclassify([0.5,0.5],group,labels,3)
    print t

if __name__=='__main__':
    main()
