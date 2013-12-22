import collections
import operator

import datasets
import features
import pagerank
import TFIDF
import clustering
# import recommend
from normalize import normalizeString, lemmatization
from helpers import sliceDict

def prepareQuery(query):
    return normalizeString(query, datasets.STOPWORDS, lemmatization).split()

def query(query, subSet, useFeatures, usePageRank, useTFIDF, useClustering, useRecommend, topN=100):
    results = {}
    prevMethod = ''

    if not useFeatures and not usePageRank and not useTFIDF and not useClustering and not useRecommend:
        return None

    query = normalizeString(query, datasets.STOPWORDS, lemmatization).split()
    print "Querying with: %r" % query

    if useFeatures:
        results['IF'] = features.queryFeatures(query, results[prevMethod].keys(), subSet)
        prevMethod = 'IF'
    if usePageRank:
        results['PR'] = pagerank.queryPageRank(query, results[prevMethod].keys(), subSet)
        prevMethod = 'PR'
    if useTFIDF:
        results['TI'] = TFIDF.queryTFIDF(query, results[prevMethod].keys(), subSet)
        prevMethod = 'TI'
    if useClustering:
        results['CL'] = clustering.queryClustering(query, results[prevMethod].keys(), subSet)
        prevMethod = 'CL'
    if useRecommend:
        results['RE'] = recommend.queryRecommend(query, results[prevMethod].keys(), subSet)
        prevMethod = 'RE'

    endresults = collections.defaultdict(float)
    # Loop through all pmid's after having ID set sliced like subSet prescribes
    for pmid in sliceDict(datasets.IDS, subSet).iterkeys():
        endresults[pmid] += results.setdefault('IF',{}).setdefault(pmid,0.0) * 0.0 # Weighted modifier, if required
        endresults[pmid] += results.setdefault('PR',{}).setdefault(pmid,0.0) * 0.0 # Weighted modifier, if required
        endresults[pmid] += results.setdefault('TI',{}).setdefault(pmid,0.0) * 0.0 # Weighted modifier, if required
        endresults[pmid] += results.setdefault('CL',{}).setdefault(pmid,0.0) * 0.0 # Weighted modifier, if required
        endresults[pmid] += results.setdefault('RE',{}).setdefault(pmid,0.0) * 0.0 # Weighted modifier, if required
        endresults[pmid] /= len(results)

    # Return the topN results, sorted descending by score
    return sorted(endresults.items(), key=operator.itemgetter(1), reverse=True)[:topN]

def suggest(query, subSet, useIndependentFeatures, usePageRank, useTFIDF, useClustering, useRecommender, topN=100):
    pass
    # requires user to select similar cluster, or do it for the user. so not taking the most similar to query but 2nd similar
