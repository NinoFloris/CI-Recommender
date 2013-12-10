from numpy import *

#abstDict = TFIDF.TFIDF(config.ABSTRACTS)

abstDict = {1 : [('la', 1), ('bo', 1), ('si', 1)],
            2: [('ra', 1), ('la', 1), ('bo', 1)],
            3: [('xz', 1), ('ry', 1), ('der', 1)],
            4: [('si', 1), ('tu', 1), ('ta', 1)]}

def searchTopXterms(x, paperID):  # parameters are integers
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
    return results  # returns list of pID tuples. Index in list is n of matches

def searchTerm(term, depth):  # searches TFIDF dict for term matches
   pass #placeholder 
  
print searchTopXterms(3, 1)
    
