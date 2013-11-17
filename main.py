# External imports #
import sys
from time import time
from collections import namedtuple, defaultdict

# Internal imports #
from recommender import dataloader

datasets_folder = 'datasets/'


print 'Loading data...'
t0 = time()
Summaries = dataloader.load(datasets_folder + 'summaries.pkl')
IDs = dataloader.load(datasets_folder + 'ids.pkl')
Citations = dataloader.load(datasets_folder + 'citations.pkl')
Abstracts = dataloader.load(datasets_folder + 'abstracts.pkl')
t1 = time()
print 'Loaded %d tuples in %fs' % (len(Summaries) + len(IDs) + len(Citations) + len(Abstracts), t1-t0)


paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])

for (id, paper_info) in Summaries.iteritems():
    Summaries[id] = paper(*paper_info)

while(1):  # keep asking for input until empty line
    author_name = raw_input("Enter author: ").decode(sys.stdin.encoding)  # unicode support
    if author_name == "":
        break

    authorScores = defaultdict(int)

    for(item) in Summaries:
        if author_name in Summaries[item].authors:
            print 'Summary:'
            print Summaries[item]
            print 'Author number: %d' % (Summaries[item].authors.index(author_name)+1)
            print 'Abstract: %r' % Abstracts[item]
            for author in Summaries[item].authors:
                authorScores[author] += 1
    for item in sorted(authorScores):
        print 'Author: \'%s\' Score: %d' % (item, authorScores[item])

    print '\n'
