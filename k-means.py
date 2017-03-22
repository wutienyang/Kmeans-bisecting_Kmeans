import random
import operator
import numpy as np 
from copy import deepcopy

class point:
    def __init__(self,listLine):
        self.feature = listLine
        self.label = None           
class label:
    def __init__(self,listLine):
        self.feature = listLine
        self.cluster = []

# 載入data
filenamme = '/Users/wy/Desktop/kmean_data.txt'
points=[]

with open (filenamme,'r') as f:
    lines = f.readlines()
    
for index, line in enumerate(lines):
    line=line.strip()   
    listLine = map(float,line.split(' '))
    # 初始化 points
    tmp = point(listLine)
    points.append(tmp)
    
# 多少維度    
dimension = len(listLine)

# 初始化 label
def initialization_label(k,points):
    labels=[]
    # random以利於隨機初始label
    new_points = deepcopy(points)
    np.random.shuffle(new_points)  
    for index, line in enumerate(new_points[:k]):
        index = label(line.feature)
        labels.append(index) 
    return labels

# show points labels and feature
def show_points(points):
    for index, item in enumerate(points):
        t=""
        for findex, fitem in enumerate(item.feature):
            t += str(findex)+':'+str(fitem)+'\t'
        print(str(index)+':'+"分類"+str(item.label)+"\tfeature-"+str(t))
        
# show labels feature        
def show_labels(labels):
    for index, item in enumerate(labels):
        t=""
        for findex, fitem in enumerate(item.feature):
            t += str(findex)+':'+str(fitem)+'\t'
        print("label"+str(index)+"\tfeature-"+str(t))

def kmeans(k,labels,points,num_basic_kmeans):
    # sse = sum of square error
    sse=0
    # 清空 label 的 cluster 便於之後重新分配點的label
    for a in range(len(labels)):
        labels[a].cluster=[]
    # step1: cluster assignment
    for a in range(len(points)):
        # 計算最小的距離之list
        tp=[]
        for b in range(len(labels)):
            point_features_error=0
            for c in range(dimension):
                point_features_error += (labels[b].feature[c]-points[a].feature[c])**2
            tp.append(point_features_error)            
        points[a].label = tp.index(min(tp))+num_basic_kmeans
        sse+=tp[tp.index(min(tp))]
        # labes 加入 被分配的點
        labels[ tp.index(min(tp)) ].cluster.append(points[a])     
        
    # step2: move centroid
    for a in range(len(labels)):
        if len(labels[a].cluster) !=0:
            for c in range(dimension):
                temp = 0
                for b in range(len( labels[a].cluster )):
                    temp+=labels[a].cluster[b].feature[c]
                labels[a].feature[c]=float(temp)/float(len(labels[a].cluster))  
                
    # return labels 用於 basic_kmeans
    return (sse , labels)

# basic_kmeans
def basic_kmeans(k,points,num_basic_kmeans,times):
    labels = optimization(k,points,times)
    psse, plabelList = kmeans(k,labels,points,num_basic_kmeans)
    sse, labelList = kmeans(k,labels,points,num_basic_kmeans)
    count=1
    while psse != sse:
        psse = sse
        sse, labelList = kmeans(k,labels,points,num_basic_kmeans)
        count += 1
    return (sse , labelList)

# costfunction 算出 sse = sum of square error
def costfunction(labels,points):
    # sse = sum of square error
    sse=0
    for a in range(len(points)):
        # 計算最小的距離之list
        tp=[]
        for b in range(len(labels)):
            point_features_error=0
            for c in range(dimension):
                point_features_error += (labels[b].feature[c]-points[a].feature[c])**2
            tp.append(point_features_error)            
        sse+=tp[tp.index(min(tp))]
    return sse

# bisecting_Kmeans
def bisecting_Kmeans(points,nbk,times):
    # 執行第一次 bisecting_Kmeans t=0
    sse,labels = basic_kmeans(2,points,0,times)
    # bisecting_Kmeans 中 points皆會分成兩類 labels[0],labels[1]
    show_points(labels[0].cluster)
    print('@@')
    show_points(labels[1].cluster)
    print('@@')
    minsseDict = {}
    clusterDict = {}
    # 假設執行num_basic_kmeans次 所需執行k-1次bisecting_Kmeans 第一次以執行，故剩下k-1-1 = k-2次
    for nbk in range(nbk-2):
        sse0 = costfunction(labels,labels[0].cluster)
        minsseDict[nbk]=sse0
        clusterDict[nbk]=labels[0].cluster
        # 一次分兩cluster 故+2避免重覆
        sse1 = costfunction(labels,labels[1].cluster)
        minsseDict[nbk+2]=sse1
        clusterDict[nbk+2]=labels[1].cluster
        # find minsseDict min value
        key = max(minsseDict.iteritems(), key=operator.itemgetter(1))[0]
        tppoints = clusterDict[key]
        del minsseDict[key]
        del clusterDict[key]
        sse,labels = basic_kmeans(2,tppoints,nbk*2+2,times)
        # 每一次去分類的points
        print('@@')
        show_points(tppoints)

# 以 first sse = sum of square error 來找出較好的初始點
def optimization(k,points,times):
    if times != 0:
        sseList=[]
        labelList=[]
        for a in range(times):
            labels = initialization_label(k,points)
            sse = costfunction(labels,points)
            sseList.append(sse)
            labelList.append(labels)
            best_labels = labelList[sseList.index(min(sseList))]
    else:
        best_labels = initialization_label(k,points)
    return best_labels

def choose_k(points,k_range,times):
    k_candidate=[]
    # 帶入k的範圍
    for k in range(1,k_range):
        best_labels = optimization(k,points,times)
        sse,labelList = basic_kmeans(k,points,0,times)
        k_candidate.append(sse)
    sse_slopeList=[0,0]
    print(k_candidate)
    for a in range(len(k_candidate)-1):
        # 算出不同k值的斜率 根據elbow 求出 best_k
        sse_slope = k_candidate[a+1]-k_candidate[a]
        sse_slopeList.append(sse_slope)
    #選出最斜率變化最大    
    best_k = sse_slopeList.index(min(sse_slopeList))
    return best_k

# basic_kmeans
basic_kmeans(4,points,0,10)
show_points(points)

# depend on elbow theorem find bestk
choose_k(points,10,10)

# bisecting_Kmeans
bisecting_Kmeans(points,4,10)
show_points(points)