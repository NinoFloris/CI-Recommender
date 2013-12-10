import collections
import cPickle
import math
from time import time

import config
from helpers import timeRun
import normalize

def TFIDF(documents):
    tfdict = {}
    dfdict = collections.defaultdict(int)
    for pmid, document in documents.iteritems():
        words = document.split()
        #skip on lower than 5 words, no data is provided or it is useless as tf-idf material
        if(len(words) < 5):
            continue

        tfdict[pmid] = TF(words)
        #combining this loop for some df as well
        for word in set(words):
            dfdict[word] += 1

    tfidfdict = {}
    idfdict = IDF(dfdict, len(documents))
    for pmid, tf in tfdict.iteritems():
        tfidfdict[pmid] = {term: (count * idfdict[term]) for term, count in tf}

    return tfidfdict

#adaptive TF = every word with its normalized value for max term, e.g. TFid = (fid / maxk fkd)
#tfrequency of word i in document d is that divided by the frequency of word k where k is the most common term in d
def TF(wordlist):
    #count all occurences of words and sort from most common to least, return list[(word,count),]
    tfrequency = collections.Counter(wordlist).most_common()
    #get the count of the most common term for this document, get first elements' count
    tmax = tfrequency[0][1]
    #return TF score per word based on the frequency of every word in tfrequency divided by tmax
    return [(f[0], float(f[1])/tmax) for f in tfrequency]

def IDF(dftermsdict, documentN):
    idfdict = {}
    for term, df in dftermsdict.iteritems():
        idfdict[term] = math.log(documentN/df, 2)

    return idfdict

t0 = time()
config.ABSTRACTS = cPickle.load(open("../datasets/abstracts.pkl", 'rb'))
t1 = time()
print 'Loaded %d tuples in %fs' % (len(config.ABSTRACTS), t1-t0)

config.STOPWORDS = cPickle.load(open("../datasets/stopwords.pkl", 'rb'))

t0 = time()
ran = timeRun(TFIDF, normalize.normalizeContent(config.ABSTRACTS, config.STOPWORDS))
t1 = time()
print "tfed %d documents in %fs and normalized in %fs" % (len(ran[1]), ran[0], t1-t0-ran[0])
raw_input()

'''
cPickle.dump(ran[1], open("../datasets/tfidfabstracts.pkl", 'wb'), cPickle.HIGHEST_PROTOCOL)
'''

