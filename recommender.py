import cPickle, bz2

from collections import namedtuple, defaultdict
from itertools import groupby


summaries_file = 'summaries.pkl.bz2'
ids_file = 'ids.pkl.bz2'
citations_file = 'citations.pkl.bz2'

Summaries = cPickle.load( bz2.BZ2File( summaries_file, 'rb' ) )

paper = namedtuple( 'paper', ['title', 'authors', 'year', 'doi'] )

print 'Loading data...\n'

for (id, paper_info) in Summaries.iteritems():
    Summaries[id] = paper( *paper_info )

author_name = raw_input("Enter author: ")

authorScores = defaultdict(int)

for(item) in Summaries:
    if author_name in Summaries[item].authors:
        print Summaries[item]
        print Summaries[item].authors.index(author_name)
        print '\n'
        for author in Summaries[item].authors:
            authorScores[author] += 1
for item in sorted(authorScores):
    print item
    print authorScores[item]


