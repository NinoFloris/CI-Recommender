import collections
import operator

import dataloader
import datasets
import searches
from helpers import sliceDict, printStarted, printTimeRun, normalizeScore


@printStarted
@printTimeRun
def queryPageRank(query, subSet, independentRun=False, topN=None):
    """Generic function to set up the datasets, and create normalized scoring (0 to 1) for a specific module technique.
    Also used when independent running of the module technique (no preprocessing of query) is wanted. 
    
    Keyword arguments:
    query -- (list/str) the processed query word list (pass a string if independentRun = True)
    subSet -- (str) supply a subset (based on globalsubset please) to the function, this is also used in retrieving/saving datasets.
    independentRun -- (bool) if a independentRun is desired this allows a string query (default False)
    topN -- (int) return the highest N results

    Returns -- sorted list: [pmid: score] of topN results (highest first).
    
    """
    citations = sliceDict(datasets.CITATIONS, subSet)
    # Debug
    # citations = {1:[2,3,4,5],2:[],3:[],4:[], 5:[]}

    citedby = dataloader.loadProcessed("citedby", "citations", subSet)
    if citedby is None:
        citedby = collections.defaultdict(list)
        print "PageRank is generating the inverse subset of citations"
        for ref, papersCitingRef in citations.iteritems():
            for pmid in papersCitingRef:
                citedby[pmid].append(ref)
        dataloader.saveProcessed(citedby, "citedby", "citations", subSet, saveBZ2=True)

    if independentRun:
        query = searches.prepareQuery(query)
        print "Querying PageRank with: %r" % query

    results = dataloader.loadProcessed("resultsPageRank", "citations-citedby", subSet)
    if results is None:
        results = pageRank(citations, citedby)
        dataloader.saveProcessed(results, "resultsPageRank", "citations-citedby", subSet, saveBZ2=True)

    normalizeScore(results)

    if independentRun:
        results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:topN]

    return results


def calculatepagerank(self,iterations=20):
    # initialize every url with a page rank of 1
    for (urlid,) in self.con.execute('select rowid from urllist'):
        self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
    self.dbcommit()

    for i in range(iterations):
        print "Iteration %d" % (i)
        for (pmid,) in self.con.execute('select rowid from urllist'):
            pr=0.15
        
            # Loop through all the pages that cite this pmid
            for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                # Get the page rank of the citer
                linkingpr=self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]

                # Get the total number of links from the citer
                linkingcount=self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                
                pr+=0.85*(linkingpr/linkingcount)
            self.con.execute('update pagerank set score=%f where urlid=%d' % (pr,urlid))
        self.dbcommit()


def pageRank(paperCitations, paperCitedBy, minDelta=0.00001, rounds=100):
    """Calculates the pagerank for every citation of the papers we have citation data of.
    When dampingFactor is 0 the sum of all ranks * nDoc should equal nDoc

    Keyword arguments:
    paperCitations -- the dict containing citations per paper (e.g. [2000000] returns (2000001, 2000045) these papers cite 2000000)
    paperCitedBy -- the inversed dict of paperCitations, the references (e.g. [2000001] returns (2000000) because it is a reference for 2000001)
    minDelta -- the minimum delta acceptable before decided that PageRank has converged (default 0.00001)
    rounds -- the amount of rounds pagerank should do, minChanges breaks out of this loop first (default 150)

    Returns -- {pmid: pagerank}

    """
    allCites = paperCitedBy.keys()
    nDoc = len(paperCitedBy)
    dampingFactor = 0.85
    
    # Initialize all pmid's to the same pagerank 1/nDoc
    ranks = dict.fromkeys(allCites, 1.0/nDoc)

    for i in xrange(rounds):
        diff = 0
        for pmid in allCites:
            pr = (1.0-dampingFactor)/nDoc

            for citerpmid in paperCitations.setdefault(pmid,{}):
                pr += dampingFactor * (ranks.setdefault(citerpmid,1.0/nDoc) / len(paperCitedBy[citerpmid]))

            diff += abs(ranks[pmid] - pr)
            ranks[pmid] = pr

        if diff < minDelta:
            print "PageRank converged after round: %d" % i
            break

    # Debug
    # print nDoc
    # print sum(ranks.values()) * nDoc

    return ranks

# Debug
# print queryPageRank('test',None,None,False,10)
