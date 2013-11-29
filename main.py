# External imports #
import sys
from time import time
from collections import namedtuple
from scipy import stats
# Internal imports #
from recommender import dataloader, distance, config

datasets_folder = 'datasets/'


print 'Loading data...'
t0 = time()
#Summaries is in format like ('Patterns of sex work contact among men in the general population of Switzerland, 1987-2000.', ['Jeannin A', 'Rousson V', 'Meystre-Agustoni G', 'Dubois-Arber F'], 2008, '10.1136/sti.2008.030031')
Summaries = dataloader.load(datasets_folder + 'summaries.pkl')
IDs = dataloader.load(datasets_folder + 'ids.pkl')
Citations = dataloader.load(datasets_folder + 'citations.pkl')
Abstracts = dataloader.load(datasets_folder + 'abstracts.pkl')
Keywords = dataloader.load(datasets_folder + 'keywords.pkl')
t1 = time()
print 'Loaded %d tuples in %fs' % (len(Summaries) + len(IDs) + len(Citations) + len(Abstracts), t1-t0)

#Create a normal 0..X counted array, we don't use the id's anyway
SequencedSummaries = []
paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
for (i, paper_info) in enumerate(Summaries.values()):
    SequencedSummaries.append(paper(*paper_info))

#this way we also only load them once
config.SUMMARIES = SequencedSummaries
config.IDS = IDs
config.CITATIONS = Citations
config.ABSTRACTS = Abstracts

while(1):  # keep asking for input until empty line
    author_name = raw_input("Enter author: ").decode(sys.stdin.encoding)  # unicode support
    if author_name == "":
        break

    for i, item in enumerate(Summaries):
        if author_name in Summaries[item].authors:
            print 'Summary:'
            print Summaries[item]
            print 'Author number: %d' % (Summaries[item].authors.index(author_name)+1)
            print 'Abstract: %r' % Abstracts[item]
    
    print '\n'
