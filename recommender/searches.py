import collections
import operator

import datasets
import features
import pagerank
import TFIDF
import clustering
# import recommend
from normalize import normalizeString, lemmatization
from helpers import sliceDict, normalizeScore

def prepareQuery(query):
    return normalizeString(query, datasets.STOPWORDS, lemmatization).split()

def query(query, subSet, useFeatures, usePageRank, useTFIDF, useClustering, useRecommend, topN=100):
    results = {}

    if not useFeatures and not usePageRank and not useTFIDF and not useClustering and not useRecommend:
        return None

    query = normalizeString(query, datasets.STOPWORDS, lemmatization).split()
    print "Querying with: %r" % query

    if useFeatures:
        results['IF'] = features.queryFeatures(query, subSet)
        prevMethod = 'IF'
    if usePageRank:
        results['PR'] = pagerank.queryPageRank(query, subSet)
    if useTFIDF:
        results['TI'] = TFIDF.queryTFIDF(query, subSet)
    if useClustering:
        results['CL'] = clustering.queryClustering(query, subSet)
        prevMethod = 'CL'
    if useRecommend:
        results['RE'] = recommend.queryRecommend(query, subSet)
        prevMethod = 'RE'


    endresults = collections.defaultdict(float)
    # Loop through all pmid's after having ID set sliced like subSet prescribes
    for pmid in [pmid for pmid in datasets.IDS if str(pmid).startswith(subSet)]:
        i = 0
        if useFeatures and results['IF'].has_key(pmid):
            i += 1
            endresults[pmid] += results['IF'][pmid] * 1.0 # Weighted modifier, if required 
        if usePageRank and results['PR'].has_key(pmid):
            i += 1
            endresults[pmid] += results['PR'][pmid] * 1.0 # Weighted modifier, if required
        if useTFIDF and results['TI'].has_key(pmid):
            i += 1 
            endresults[pmid] += results['TI'][pmid] * 1.0 # Weighted modifier, if required
        if useClustering and results['CL'].has_key(pmid):
            i += 1 
            endresults[pmid] += results['CL'][pmid] * 1.0 # Weighted modifier, if required
        if useRecommend and results['RE'].has_key(pmid):
            i += 1 
            endresults[pmid] += results['RE'][pmid] * 1.0 # Weighted modifier, if required
        if i > 0:
            endresults[pmid] /= i # Divide by the amount of succesful techniques ran on this pmid

    normalizeScore(endresults)
    # Return the topN results, sorted descending by score
    return sorted(endresults.items(), key=operator.itemgetter(1), reverse=True)[:topN]

def suggest(query, subSet, useIndependentFeatures, usePageRank, useTFIDF, useClustering, useRecommender, topN=100):
    pass
    # requires user to select similar cluster, or do it for the user. so not taking the most similar to query but 2nd similar
