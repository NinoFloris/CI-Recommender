# External imports #
from flask import Flask
from flask import render_template, request, jsonify
from collections import namedtuple
from collections import defaultdict
from time import time
# Internal imports #
from recommender import dataloader, distance, config

app = Flask(__name__)
app.debug = True

datasets_folder = 'datasets/'

@app.route('/')
def index():
    return render_template('index.html')

#The real deal starts here
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    query = request.json['query']
    querytype = request.json['type']
    # do something with the query here; main recommending function
    # results = distance.getRecommendedAuthors(config.SUMMARIES,query)
    # return a list of recommended papers with e.g. scores and stuff
    return jsonify({"query" : query, "type" : querytype})



if __name__ == '__main__':
    '''
    paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
    print 'Loading data...'
    t0 = time()

    #gibberjabber about turning summaries into a dict of authors with their titles
    Summaries = defaultdict(list)
    for paper_info in dataloader.load(datasets_folder + 'summaries.pkl').itervalues():
        Summaries[paper(*paper_info).title] = dict({author: 0.0 for author in paper(*paper_info).authors})
    Summaries = distance.transformDict(Summaries, "E")

    #CURRENTLY NOT! Summaries is in format like ('Patterns of sex work contact among men in the general population of Switzerland, 1987-2000.', ['Jeannin A', 'Rousson V', 'Meystre-Agustoni G', 'Dubois-Arber F'], 2008, '10.1136/sti.2008.030031')
    config.SUMMARIES = Summaries
    config.IDS = dataloader.load(datasets_folder + 'ids.pkl')
    config.CITATIONS = dataloader.load(datasets_folder + 'citations.pkl')
    config.ABSTRACTS = dataloader.load(datasets_folder + 'abstracts.pkl')
    config.KEYWORDS = dataloader.load(datasets_folder + 'keywords.pkl')
    t1 = time()
    print 'Loaded %d tuples in %fs' % (len(config.SUMMARIES) + len(config.IDS) + len(config.CITATIONS) + len(config.ABSTRACTS) + len(config.KEYWORDS), t1-t0)
    '''
    app.run()





