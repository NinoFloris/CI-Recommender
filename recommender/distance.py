import cPickle, bz2
import re
import math
import collections
from itertools import groupby

#summaries_file = 'summaries.pkl.bz2'
#ids_file = 'ids.pkl.bz2'
#citations_file = 'citations.pkl.bz2'
abstracts_file = 'abstracts.pkl.bz2'

print 'Loading data...\n'

Abstracts = cPickle.load( bz2.BZ2File( abstracts_file, 'rb' ) )

def getwords(doc):
    splitter = re.compile('\\W*')
    words = [s.lower() for s in splitter.split(doc)  if len(s) > 4 and len(s) < 20]
    dict = {}
    for w in words:
        dict[w] = words.count(w)
    return dict 

def distance(pIDx, pIDy):
    splitter = re.compile('\\W*')
    words1 = [s.lower() for s in splitter.split(Abstracts[pIDx])  if len(s) > 4 and len(s) < 20]
    words2 = [s.lower() for s in splitter.split(Abstracts[pIDy])  if len(s) > 4 and len(s) < 20]
    list1 = []
    list2 = []
    for w in words1:
        if [words1.count(w), w] not in list1:
            list1.append([words1.count(w), w])
    for w in words2:
        if [words1.count(w), w] not in list2:
            list2.append([words2.count(w), w])
    list1 = sorted(list1, reverse=True)[:5]
    list2 = sorted(list2, reverse=True)[:5]
    matchCount = 0
    for value in list1:
        if value in list2:
            print "\nMatch found: "
            print value
            matchCount += 1
    return matchCount

print distance(Abstracts.keys()[22], Abstracts.keys()[18])
