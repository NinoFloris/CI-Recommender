import collections
import math
import operator

import dataloader
import datasets
import searches
from normalize import normalizeDocuments, lemmatization
from helpers import sliceDict, printStarted, printTimeRun, normalizeScore


@printStarted
@printTimeRun
def queryTFIDF(query, subSet, independentRun=False, topN=None):
    """Generic function to set up the datasets, and create normalized scoring (0 to 1) for a specific module technique.
    Also used when independent running of the module technique (no preprocessing of query) is wanted. 
    
    Keyword arguments:
    query -- (list/str) the processed query word list (pass a string if independentRun = True)
    subSet -- (str) supply a subset (based on globalsubset please) to the function, this is also used in retrieving/saving datasets.
    independentRun -- (bool) if a independentRun is desired this allows a string query (default False)
    topN -- (int) return the highest N results

    Returns -- sorted list: [pmid: score] of topN results (highest first).
    
    """
    abstracts = {}
    titles = {}
    merged = {}

    titles = dataloader.loadProcessed("normalized", "titles", subSet)
    if titles is None:
        print "TFIDF is generating the processed subset of SUMMARIES"
        titles = {pmid: paper_info.title for pmid, paper_info in datasets.SUMMARIES.iteritems()}
        titles = sliceDict(titles, subSet)
        titles = normalizeDocuments(titles, datasets.STOPWORDS, lemmatization)
        dataloader.saveProcessed(titles, "normalized", "titles", subSet, saveBZ2=True)

    abstracts = dataloader.loadProcessed("normalized", "abstracts", subSet)
    if abstracts is None:
        print "TFIDF is generating the processed subset of ABSTRACTS"
        abstracts = sliceDict(datasets.ABSTRACTS, subSet)
        abstracts = normalizeDocuments(abstracts, datasets.STOPWORDS, lemmatization)
        dataloader.saveProcessed(abstracts, "normalized", "abstracts", subSet, saveBZ2=True)

    if independentRun:
        query = searches.prepareQuery(query)
        print "Querying TFIDF with: %r" % query

    merged = dataloader.loadProcessed("mergedTFIDF", "titles-abstracts", subSet)
    if merged is None:
        merged = {}
        for pmid, doc in titles.iteritems():
            merged[pmid] = doc + abstracts[pmid]
        # Finally run tfidf
        merged = TFIDF(merged)
        dataloader.saveProcessed(merged, "mergedTFIDF", "titles-abstracts", subSet, saveBZ2=True)

    results = {}
    for pmid, tfidfscores in merged.iteritems():
        score = 0.0
        for term, termscore in tfidfscores.iteritems():
            for qword in query:
                if qword in term:
                    score += termscore
                    
        results[pmid] = score

    normalizeScore(results)

    if independentRun:
        results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:topN]

    return results

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
        # Combining this loop for some df as well
        for word in set(words):
            dfdict[word] += 1

    tfidfdict = {}
    idfdict = IDF(dfdict, len(documents))
    for pmid, tf in tfdict.iteritems():
        tfidfdict[pmid] = {term: (count * idfdict[term]) for term, count in tf}

    return tfidfdict

def TF(termList):
    """Calculates the TF score for every word in the given list.
    Uses relative TF, every word with its normalized value for max term in document, TFid = (fid / maxk fkd).
    TF of word i in document d is that divided by the frequency of word k where k is the most common term in d

    Keyword arguments:
    termList -- the list of terms

    Returns -- list: [(term, score)]

    """
    # Use counter collection to get term frequency for all terms, sort on most_common, get tmax and calculate scores
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
