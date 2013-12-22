import cPickle, bz2
import re
import math
import collections
from itertools import groupby
import clustering, config
from math import sqrt

def pearson(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)
    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])
    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0
    return 1.0-num/den


def getDistances(data, v1):
    distancelist=[]
    for i in range(len(data)):
        v2=data[i]
        distancelist.append((euclidean(v1, v2), i))
        distancelist.sort()
    return distancelist

def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

def knnEstimate(data,vec1,k=3):
    # Get sorted distances
    dlist=getDistances(data, vec1)
    avg=0.0
    # Take the average of the top k results
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]
        avg=avg/k
    return avg

def transformDict(data):
    result={}
    for key in data:
        for val in data[key]:
            result.setdefault(val,{})
            result[val][key] = 0.0
    return result




