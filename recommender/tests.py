from time import time

import clustering
import config
import dataloader
import distance
import helpers
import normalize
import pagerank
import searches
import TFIDF

#Start by loading in all our datasets
dataloader.addToConfig(dataloader.loadAll())

def TFIDFTest():
    t0 = time()
    ran = helpers.timeRun(TFIDF, normalize.normalizeContent(config.ABSTRACTS, config.STOPWORDS))
    t1 = time()
    print "tfed %d documents in %fs and normalized in %fs" % (len(ran[1]), ran[0], t1-t0-ran[0])

def pageRankTest():
    print pagerank.pagerank(config.CITATIONS, config.CITEDBY, 10, 150)

def searchesTest():
    # slicing the dict for the search
    d = TFIDF.TFIDF(normalize.normalizeContent(helpers.slicedict(config.ABSTRACTS, 'A'), config.STOPWORDS))
    searches.searchTopXterms(d, 10, config.ABSTRACTS.iterkeys().next())
    print searches.searchTopXterms(3, 1)

def ClusteringTest():
    testDict = helpers.sliceDict(config.CITATIONS,'201')
    # clusterPoints1 = clustering.createFirstCentroid(config.CITATIONS,5)
    # print(clusterPoints1)
    print(clustering.cluster(5, testDict, dist, 5, 10))


def dist(a,b):
    return a+b/3

# TFIDFTest()
# pagerank()
# searchesTest()
ClusteringTest()

# pickle an object #
#cPickle.dump(pagerank.citedBy(config.CITATIONS), open("../datasets/citedby.pkl", 'wb'), cPickle.HIGHEST_PROTOCOL)
