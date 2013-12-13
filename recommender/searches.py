import math
import config
from numpy import *

#abstDict = TFIDF.TFIDF(config.ABSTRACTS)
abstDict = {1 : [('la', 1), ('bo', 1), ('si', 1)],
            2: [('ra', 1), ('la', 2), ('bo', 1)],
            3: [('xz', 1), ('ry', 1), ('der', 1)],
            4: [('si', 1), ('la', 3), ('ta', 1)]}

Summaries = config.SUMMARIES

def searchTopXterms(x, paperID): #this function recommends papers on paper input based on TFIDF output
    results = [[]] * (x+1)
    terms = []
    for i in range(0, x):
        terms.append(abstDict[paperID][i][0])
    print terms
    print "\n"
    for pID in abstDict:
        count = 0
        for i in range(0, x):
            print results
            if abstDict[pID][i][0] in terms:
                count += 1
                print abstDict[pID][i][0]
                print "in terms \n"
        results[count] = results[count] + [pID]
    return results #returns list of pID tuples. Index in list is n of matches

def searchTermTitle(term):  # searches Summaries for term matches
    results = []
    for paper in config.SUMMARIES:
        if term in paper[0]: #is term in title?
            results.append(paper[0]);
    return results

def searchAuthor(author):
    results = []
    for paper in config.SUMMARIES
        if author in paper[1]:
            results.append(paper)
    return results

def searchTermTFIDF(term):
    results = []
    for pID in abstDict:
        for item in abstDict[pID]:
            for termScore in item:
                if term in termScore:
                    results.append((termscore[1], Summaries[pID]))
    return sorted(results, key=lambda tup: tup[0])   #sort based on first element


#print searchTermTitle('virus');
#print searchTopXterms(3, 1)
    
