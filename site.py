# External imports #
from flask import Flask
from flask import render_template, request, jsonify
from collections import namedtuple
from collections import defaultdict
from time import time
# Internal imports #
from recommender import dataloader, distance, config, TFIDF

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

#The real deal starts here
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    query = request.json['query']
    querytype = request.json['type']

    tfidfresults = []
    for (pmid, score) in TFIDF.queryTFIDF(query, '20'):
        print "PubmedID: %d Scored: %f" % (pmid, score)
        print "Title: %r" % config.SUMMARIES[pmid].title
        tfidfresults.append({'pmid': pmid, 'score':score,'title':config.SUMMARIES[pmid].title})

    # do something with the query here; main recommending function
    # results = distance.getRecommendedAuthors(config.SUMMARIES,query)
    # return a list of recommended papers with e.g. scores and stuff
    return jsonify(results=tfidfresults)



if __name__ == '__main__':
    '''
    #gibberjabber about turning summaries into a dict of authors with their titles
    Summaries = defaultdict(list)
    for paper_info in dataloader.load(datasets_folder + 'summaries.pkl').itervalues():
        Summaries[paper(*paper_info).title] = dict({author: 0.0 for author in paper(*paper_info).authors})
    Summaries = distance.transformDict(Summaries, "E")
    '''
    dataloader.addToConfig(dataloader.loadAll())

    #Summaries is in format like ('Patterns of sex work contact among men in the general population of Switzerland, 1987-2000.', ['Jeannin A', 'Rousson V', 'Meystre-Agustoni G', 'Dubois-Arber F'], 2008, '10.1136/sti.2008.030031')
    paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
    for (pmid, paper_info) in config.SUMMARIES.iteritems():
        config.SUMMARIES[pmid] = paper( *paper_info )

    app.run()





