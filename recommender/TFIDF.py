import collections
import math
import operator
import dataloader

import config

from normalize import normalizeString, normalizeDocuments, lemmatization
from helpers import sliceDict, printStarted, printTimeRun


@printStarted
@printTimeRun
def queryTFIDF(query, subSet=None, topN=10):
    abstracts = {}
    titles = {}
    merged = {}

    titles = dataloader.loadProcessed("normalized", "titles", subSet)
    if titles is None:
        titles = {pmid: paper_info.title for pmid, paper_info in config.SUMMARIES.iteritems()}
        titles = sliceDict(titles, subSet)
        titles = normalizeDocuments(titles, config.STOPWORDS, lemmatization)
        dataloader.saveProcessed(titles, "normalized", "titles", subSet, saveBZ2=True)

    abstracts = dataloader.loadProcessed("normalized", "abstracts", subSet)
    if abstracts is None:
        abstracts = sliceDict(config.ABSTRACTS, subSet)
        abstracts = normalizeDocuments(abstracts, config.STOPWORDS, lemmatization)
        dataloader.saveProcessed(abstracts, "normalized", "abstracts", subSet, saveBZ2=True)

    qwords = normalizeString(query, config.STOPWORDS, lemmatization).split()
    print "Querying with (after normalization and query expansion): %r" % qwords

    #prune titles with OR search
    # remove = []
    # for pmid, title in titles.iteritems():
    #     keep = False
    #     for word in qwords:
    #         if word in title or word in abstracts[pmid]:
    #             keep = True
    #     if not keep:
    #         remove.append(pmid)
    # for pmid in remove:
    #     del titles[pmid]
    #     del abstracts[pmid]

    # del remove[:]

    merged = dataloader.loadProcessed("mergedTFIDF", "titles-abstracts", subSet)
    if merged is None:
        merged = {}
        for pmid, doc in titles.iteritems():
            merged[pmid] = doc + abstracts[pmid]
        #finally run tfidf
        merged = TFIDF(merged)
        dataloader.saveProcessed(merged, "mergedTFIDF", "titles-abstracts", subSet, saveBZ2=True)

    results = {}
    for pmid, tfidfscores in merged.iteritems():
        score = 0.0
        for term, termscore in tfidfscores.iteritems():
            for word in qwords:
                if word in term:
                    score += termscore
        results[pmid] = score

    end = sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:topN]
    # for (pmid, score) in end:
    #     print merged[pmid]

    return end

def TFIDF(documents):
    """Calculates the TFIDF score for every document's terms.

    Keyword arguments:
    documents -- (dict) documents {id: document}

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
    dfTermsDict -- (dict) document frequency {term: inNdocuments} (e.g. "Space" occurred in 10 documents)
    documentN -- the amount of documents to divide the document frequency by

    Returns -- dict: {term: score}

    """
    idfdict = {}
    for term, df in dfTermsDict.iteritems():
        idfdict[term] = math.log(documentN/df, 10)

    return idfdict
