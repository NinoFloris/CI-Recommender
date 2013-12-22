import collections

import datasets
from helpers import sliceDict

#abstDict = TFIDF.TFIDF(config.ABSTRACTS)
abstDict = {1 : [('la', 1), ('bo', 1), ('si', 1)],
            2: [('ra', 1), ('la', 2), ('bo', 1)],
            3: [('xz', 1), ('ry', 1), ('der', 1)],
            4: [('si', 1), ('la', 3), ('ta', 1)]}

def query(query, subSet, useIndependentFeatures, usePageRank, useTFIDF, useClustering, useRecommender, topN=100):
    results = {}
    prevMethod = ''

    if not useIndependentFeatures and not usePageRank and not useTFIDF and not useClustering and not useRecommender:
        return None

    query = normalizeString(query, datasets.STOPWORDS, lemmatization).split()
    print "Querying with: %r" % query

    if useIndependentFeatures:
        results['IF'] = queryIndependentFeatures(query, results[prevMethod].keys(), subSet)
        prevMethod = 'IF'
    if usePagerank:
        results['PR'] = queryPageRank(query, results[prevMethod].keys(), subSet)
        prevMethod = 'PR'
    if useTFIDF:
        results['TI'] = queryTFIDF(query, results[prevMethod].keys(), subSet)
        prevMethod = 'TI'
    if useClustering:
        results['CL'] = queryClustering(query, results[prevMethod].keys(), subSet)
        prevMethod = 'CL'
    if useRecommender:
        results['RE'] = queryRecommender(query, results[prevMethod].keys(), subSet)
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

def recommend(query, subSet, useIndependentFeatures, usePageRank, useTFIDF, useClustering, useRecommender, topN=100):
    pass
    # requires user to select similar cluster, or do it for the user. so not taking the most similar to query but 2nd similar
