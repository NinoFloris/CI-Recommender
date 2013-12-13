import cPickle, bz2
import re
import math
import collections
from itertools import groupby
import clustering, config
from math import sqrt

# Returns the Pearson correlation coefficient for p1 and p2
def getPearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]: 
      if item in prefs[p2]: si[item]=1

    # if they are no ratings in common, return 0
    if len(si)==0: return 0

    # Sum calculations
    n=len(si)

    # Sums of all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	

    # Sum of the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r    

def getPapers(pID):
    print "starting getpapers...\n"
    abstractWords = getwords(config.ABSTRACTS[pID])    
    titleWords = getwords(config.RAWSUMMARIES[pID][0]) #title
    for paperID in config.RAWSUMMARIES:
        score = wordMatch(titleWords, getwords(config.RAWSUMMARIES[paperID][0]))    # compare based on title
        if score > 3:
            print "\nMatch found:"
            print config.RAWSUMMARIES[paperID][0]

def termSearch(term):
    for paperID in config.ABSTRACTS:
        abstractWords = getwords(config.ABSTRACTS[paperID])
        for word in abstractWords:
            if word == term:
                print "\nMatch found:"
                print config.RAWSUMMARIES[paperID][0]

def topMatches(prefs,person,n=5,similarity=getPearson):
    scores=[(similarity(prefs,person,other),other)for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

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

#deprecated, use Counter(document.split()) or TF(document.split())
def getWords(doc):
    splitter = re.compile('\\W*')
    words = [s.lower() for s in splitter.split(doc)  if len(s) > 4 and len(s) < 20]
    dict = {}
    for w in words:
        dict[w] = words.count(w)
    return dict

def getRecommendedAuthors(itemMatch, author_name):
    userRatings = []   
    for i, item in enumerate(config.SUMMARIES):
        if author_name in config.SUMMARIES[i].authors:
            userRatings.append(config.SUMMARIES[i].authors)

    for item in userRatings:
        print item

    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings:
    # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    # Divide each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings
