import random

"""
    This function makes cluster from data and a function that tell a distance within those data
    The first argument gives the number of clusters we want at the end
    The second argument are the data
    The third one is the distance function
    The result is an array that contain a number of cluster for each element from the second argument in the same order
"""

def cluster(numOfClusters, stdSet, distFunction):
    centroids = createFirstCentroid(stdSet, numOfClusters)
    rounds = 0
    clusterArray = []
    changes = 10
    while(changes>2 or rounds<150):    #If there is less than 2 changes, we stop the algorithm, same thing if it is running since more than 150 loops
        changes = 0
        for i in range(stdSet.length):
            minDist = distFunction(stdSet[i], stdSet[centroids[0]])     #stdSet[i] is one element to put in a cluster
            cluster = 0
            for j in range(numOfClusters-1):
                currentDist = distFunction(stdSet[i],stdSet[centroids[i+1]])
                if currentDist < minDist :
                    minDist = currentDist
                    cluster = j
            if clusterArray[i] != j :
                clusterArray[i] = j
                changes += 1
            rounds += 1
        centroids = updatecentroids(stdSet, clusterArray, distFunction, numOfClusters)
    return clusterArray


"""
    This function create the first clusters to init the recursive algorithm
    The first argument is the set from where to randomly take the initial elements
    The second argument is the number of elements to return
    The result return is the ID of the cluster centroid within the stdSet
"""

def createFirstCentroid(stdSet,number):
    answer = [number]
    for i in range(number):
        answer[i] = random.randint(1, stdSet.length)
    return answer


"""
    This function update the clusters centroid position depending on the previous algorithm step.
    For now it return a paper from the set which is the less far from the others
    The first argument is the previous cluster centroids set
    The second argument is the stdSet of papers, or author, or whatever
"""

def updatecentroids(stdSet, clusterArray, distFunction, numOfClusters):
    centroids[numOfClusters]
    for i in range(numOfClusters):
        minDist = 0
        futureCentroid = -1
        for j in range(stdSet.length):
            dist = 0
            for k in range(stdSet.length):
                if clusterArray[j] == clusterArray[k]:  #Only if they are in the same cluster we add the distance to the distance for this point
                    dist += distFunction(stdSet[j],stdSet[k])
            if dist < minDist or futureCentroid == -1:
                minDist = dist
                futureCentroid = j
        centroids[i] = futureCentroid
    return centroids
