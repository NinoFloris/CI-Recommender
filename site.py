# External imports #
from flask import Flask
from flask import render_template, request, jsonify
from collections import namedtuple
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
    # print 'Loading data...'
    # t0 = time()
    # #Create a normal 0..X counted array, we don't use the id's anyway
    # Summaries = []
    # paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
    # for (i, paper_info) in enumerate(dataloader.load(datasets_folder + 'summaries.pkl').values()):
    #     Summaries.append(paper(*paper_info))
    # #Summaries is in format like ('Patterns of sex work contact among men in the general population of Switzerland, 1987-2000.', ['Jeannin A', 'Rousson V', 'Meystre-Agustoni G', 'Dubois-Arber F'], 2008, '10.1136/sti.2008.030031')
    # config.SUMMARIES = Summaries
    # config.IDS = dataloader.load(datasets_folder + 'ids.pkl')
    # config.CITATIONS = dataloader.load(datasets_folder + 'citations.pkl')
    # config.ABSTRACTS = dataloader.load(datasets_folder + 'abstracts.pkl')
    # config.KEYWORDS = dataloader.load(datasets_folder + 'keywords.pkl')
    # t1 = time()
    # print 'Loaded %d tuples in %fs' % (len(config.SUMMARIES) + len(config.IDS) + len(config.CITATIONS) + len(config.ABSTRACTS) + len(config.KEYWORDS), t1-t0)

    app.run()





