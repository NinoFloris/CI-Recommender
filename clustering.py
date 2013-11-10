import random

"""
    This function makes cluster from data and a function that tell a distance within those data
    The first argument gives the number of clusters we want at the end
    The second argument are the data
    The third one is the distance function
    The result is an array that contain a number of cluster for each element from the second argument in the same order
"""

def cluster(numberOfClusters, set, distFunction):
    clusterPoints = createFirstClusters(set, numberOfClusters)
    numberOfRounds = 0
    clusterArray = []
    numberOfChanges = 0
    while(numberOfChanges>2 and numberOfRounds<150):    #If there is less than 2 changes, we stop the algorithm, same thing if it is running since more than 150 loops
        numberOfChanges = 0
        for i in range(set.length):
            minDist = distFunction(set[i], set[clusterPoints[0]])     #set[i] is one element to put in a cluster
            cluster = 0
            for j in range(numberOfClusters-1):
                currentDist = distFunction(set[i],set[clusterPoints[i+1]])
                if currentDist < minDist :
                    minDist = currentDist
                    cluster = j
            if clusterArray[i] != j :
                clusterArray[i] = j
                numberOfChanges += 1
            numberOfRounds += 1
        clusterPoints = updateClusterPoints(clusterArray, set, clusterArray, distFunction)
    return clusterArray


"""
    This function create the first clusters to init the recursive algorithm
    The first argument is the set from where to randomly take the initial elements
    The second argument is the number of elements to return
    The result return is the ID of the cluster centroid within the set
"""

def createFirstClusters(set,number):
    answer = [number]
    for i in range(number):
        answer[i] = random.randint(1, set.length)
    return answer


"""
    This function update the clusters centroid position depending on the previous algorithm step.
    For now it return a paper from the set which is the less far from the others
    The first argument is the previous cluster centroids set
    The second argument is the set of papers
"""

def updateClusterPoints(clusters, set, clusterArray, distFunction):
    for i in range(clusters.length):
        minDist = 0
        futureCentroid = -1
        for j in range(set.length):
            dist = 0
            for k in range(set.length):
                if clusterArray[j] == clusterArray[k]:  #Only if they are in the same cluster we add the distance to the distance for this point
                    dist += distFunction(set[j],set[k])
            if dist < minDist or futureCentroid == -1:
                minDist = dist
                futureCentroid = j
        cluster[i] = futureCentroid
    return clusters