import sys
from collections import namedtuple

from recommender import dataloader, distance, config, searches, TFIDF

#Start by loading in all our datasets
dataloader.addToConfig(dataloader.loadAll("datasets/"))

#Summaries is in format like ('Patterns of sex work contact among men in the general population of Switzerland, 1987-2000.', ['Jeannin A', 'Rousson V', 'Meystre-Agustoni G', 'Dubois-Arber F'], 2008, '10.1136/sti.2008.030031')
paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
for (pmid, paper_info) in config.SUMMARIES.iteritems():
    config.SUMMARIES[pmid] = paper( *paper_info )

for (pmid, score) in TFIDF.queryTFIDF("virus", '20'):
    print "PubmedID: %d Scored: %f" % (pmid, score)
    print "Title: %r" % config.SUMMARIES[pmid].title

while(0):  # keep asking for input until empty line
    author_name = raw_input("Enter author: ").decode(sys.stdin.encoding)  # unicode support
    if author_name == "":
        break

    for i, item in enumerate(config.SUMMARIES):
        if author_name in config.SUMMARIES[item][1]:
            print 'Summary:\n'
            print item
            print config.SUMMARIES[item]
            print 'Author number: %d' % (config.SUMMARIES[item][1].index(author_name)+1)
            print 'Abstract: %r' % config.ABSTRACTS[item]
    
    print '\n'
