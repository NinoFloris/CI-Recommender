def searchTopNterms(TFIDFDict, nAmount, paperID):  # parameters are integers
    results = []
    terms = Counter(TFIDFDict[paperID]).most_common()[nAmount:]
    print terms
    print "\n"
    for pID in TFIDFDict:
        count = 0
        for i in range(0, x):
            print results
            if TFIDFDict[pID][i][0] in terms:
                count += 1
                print TFIDFDict[pID][i][0]
                print "in terms \n"
        results[count] = results[count] + [pID]
    return results  # returns list of pID tuples. Index in list is n of matches


def searchTerm(term, depth):  # searches TFIDF dict for term matches
    pass  # placeholder
