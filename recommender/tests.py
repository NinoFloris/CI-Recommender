import clustering
import pagerank
import normalize
import cPickle
import config
from time import time
from helpers import timeRun



t0 = time()
config.ABSTRACTS = cPickle.load(open("../datasets/abstracts.pkl", 'rb'))
config.CITATIONS = cPickle.load(open("../datasets/citations.pkl", 'rb'))
t1 = time()
print 'Loaded %d tuples in %fs' % (len(config.ABSTRACTS), t1-t0)

#cPickle.dump(pagerank.citedBy(config.CITATIONS), open("../datasets/citedby.pkl", 'wb'), cPickle.HIGHEST_PROTOCOL)
#print "Pickled citedby"

config.CITEDBY = cPickle.load(open("../datasets/citedby.pkl", 'rb'))

t = timeRun(pagerank.pagerank, config.CITATIONS, config.CITEDBY, 10, 150)
print 'Ran pagerank in %fs' % t[0]
print t[1]