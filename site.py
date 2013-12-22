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
    return render_template('index.html', gsubset=config.SUBSET)

#The real deal starts here
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    # either true/false
    useIndependentFeatures = request.json['uif']
    usePagerank            = request.json['pagerank']
    useTFIDF               = request.json['tfidf']
    useClustering          = request.json['clustering']
    useRecommender         = request.json['recommender']

    # 10, 25, 50, 100
    numResults = request.json['results']

    # the query string
    query = request.json['query']

    # query type (0 = query, 1 = suggestion)
    querytype = request.json['type']

    # if querytype == 0:
    #     results = query(query, config.SUBSET, useIndependentFeatures, usePagerank, useTFIDF, useClustering, useRecommender, numResults)
    # elif querytype == 1:
    #     results = suggest(query, config.SUBSET, useIndependentFeatures, usePagerank, useTFIDF, useClustering, useRecommender, numResults)

    return jsonify(results=None)



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





