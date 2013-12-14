import collections
import random

def cluster(numOfClusters, stdSet, distFunction, minChanges=10, maxRounds=150):
    """Makes cluster from data and a function that tell a distance within those data

    numOfClusters -- the number of clusters we want at the end
    stdSet -- the dictionnary containing the data
    distFunction -- the distance function taking as parameter 2 id

    Returns -- tuple: (rounds=int, {pmid: cluster number})
    """
    clusters = {}
    centroids = createFirstCentroid(stdSet, numOfClusters)
    rounds = 0
    changes = minChanges + 1
    firstLoop = True
    while(changes>minChanges and rounds<maxRounds):
        #If there is less than 2 changes, we stop the algorithm, same thing if it is running since more than 150 loops
        changes = 0
        rounds += 1
        print rounds
        for pmel in stdSet.iteritems():
            pmid = pmel[0]
            #All elements are getting attributed to a cluster
            minDist = distFunction(pmid, centroids[0])
            closest = 0
            for i in range(numOfClusters-1):
                #We try to find the closest centroid (j is the cluster number)
                currentDist = distFunction(pmid,centroids[i+1])
                if currentDist < minDist :
                    minDist = currentDist
                    closest = i+1
            if firstLoop or clusters[pmid] != closest :
                #If the cluster number is different, we register a change
                clusters[pmid] = closest
                changes += 1
        if firstLoop:
            # We could have done a "do {} while" instead, but i don't know if it works in python
            firstLoop = False
        centroids = updatecentroids(clusters, distFunction, numOfClusters)
    return clusters


def createFirstCentroid(stdSet,number):
    """ Create the first clusters to init the recursive algorithm

    stdSet -- the dictionnary
    number -- the number of elements to return

    Returns -- array [rand pmid, rand pmid, ...]
    """
    answer = [0]*number
    for i in range(number):
        flag = True
        while (flag):
            # While the ID is already choosen, we loop to get a free one
            flag = False
            randID = random.choice(stdSet.keys())
            if randID in answer:
                flag = True
        answer[i] = randID
    return answer


#
#   TO BE FIXED : updatecentroids
#

def updatecentroids(cluster, distFunction, numOfClusters):
    """ Update the clusters centroid position depending on the previous algorithm step

    stdSet -- dictionnary of papers, or author, or whatever
    cluster -- the previous cluster centroids set
    distFunction -- the distance function taking as parameter 2 id
    numOfClusters -- number of clusters

    Returns -- array [centroid 1, centroid 2, ...]
    """
    centroids = [0]*numOfClusters
    for i in range(numOfClusters):
        minDist = 0
        futureCentroid = -1
        for pmid1, cluster1 in cluster.iteritems():
            dist = 0
            for pmid2, cluster2 in cluster.iteritems():
                # Only if they are in the same cluster we add the distance to the distance for this point
                # We calculate here the global distance between this point and all of the others of the cluster
                if cluster1 == cluster2:
                    dist += distFunction(pmid1,pmid2)
            if dist < minDist or futureCentroid == -1:
                # Change the distance if it is new or smaller than the previous one
                minDist = dist
                futureCentroid = pmid1
        centroids[i] = futureCentroid
    return centroids
