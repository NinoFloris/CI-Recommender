import collections
import math
import operator

import config

from normalize import normalizeContent
from helpers import sliceDict, started, timeRun


@started
@timeRun
def queryTFIDF(query, subSet=None, topN=10):
    abstracts = config.ABSTRACTS
    titles = {}
    for (pmid, paper_info) in config.SUMMARIES.iteritems():
            titles[pmid] = paper_info.title

    if subSet:
        titles = sliceDict(titles, subSet)
        abstracts = sliceDict(abstracts, subSet)
    print "subset consists of %d elements" % len(titles)

    #little hack, no time..
    qwords = [normalizeContent({'q': query}, config.STOPWORDS)['q']]

    #normalize
    titles = normalizeContent(titles, config.STOPWORDS)
    abstracts = normalizeContent(abstracts, config.STOPWORDS)

    #prune titles with OR search
    remove = []
    for pmid, title in titles.iteritems():
        keep = False
        for word in qwords:
            if word in title:
                keep = True
        if not keep:
            remove.append(pmid)
    for pmid in remove:
        del titles[pmid]

    #prune abstracts with OR search
    remove = []
    for pmid, abstract in abstracts.iteritems():
        keep = False
        for word in qwords:
            if word in abstract:
                keep = True
        if not keep:
            remove.append(pmid)
    for pmid in remove:
        del abstracts[pmid]

    del remove[:]

    #finally run tfidf
    titles = TFIDF(titles)
    abstracts = TFIDF(abstracts)
    results = {}

    for pmid, tfidfscores in titles.iteritems():
        score = 0.0
        for word in qwords:
            for term, termscore in tfidfscores.iteritems():
                if word in term:
                    score += termscore
        results[pmid] = score

    for pmid, tfidfscores in abstracts.iteritems():
        score = 0.0
        for word in qwords:
            for term, termscore in tfidfscores.iteritems():
                if word in term:
                    score += termscore
        results[pmid] = score + results.setdefault(pmid, 0)

    return sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:topN]



def TFIDF(documents):
    """Calculates the TFIDF score for every document's terms.

    Keyword arguments:
    documents -- the documentent dictionary {id: document}

    Returns -- dict: {id: {term: score}}

    """
    tfdict = {}
    dfdict = collections.defaultdict(int)
    for pmid, document in documents.iteritems():
        words = document.split()

        if(len(words) == 0):
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

def TF(termList):
    """Calculates the TF score for every word in the given list.
    Uses adaptive TF, every word with its normalized value for max term, TFid = (fid / maxk fkd).
    TF of word i in document d is that divided by the frequency of word k where k is the most common term in d

    Keyword arguments:
    termList -- the list of terms

    Returns -- list: [(term, score)]

    """
    #use counter collection to get term frequency for all terms, sort on most_common, get tmax and calculate scores
    tfrequency = collections.Counter(termList).most_common()
    if len(tfrequency) == 0:
        return []
    tmax = tfrequency[0][1]

    return [(f[0], float(f[1])/tmax) for f in tfrequency]

def IDF(dfTermsDict, documentN):
    """Calculates the IDF score for every term in the document frequency dictionary.

    Keyword arguments:
    dfTermsDict -- the dictionary {term: inNdocuments} (e.g. "Space" occurred in 10 documents)
    documentN -- the amount of documents to divide the document frequency by

    Returns -- dict: {term: score}

    """
    idfdict = {}
    for term, df in dfTermsDict.iteritems():
        idfdict[term] = math.log(documentN/df, 2)

    return idfdict
