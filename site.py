from flask import Flask
from flask import render_template, request, jsonify
import json

from recommender import searches, config, TFIDF, datasets

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', gsubset=config.SUBSET)

#The real deal starts here
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    # either true/false
    useIndependentFeatures = json.loads(request.json['uif'])
    usePagerank            = json.loads(request.json['pagerank'])
    useTFIDF               = json.loads(request.json['tfidf'])
    useClustering          = json.loads(request.json['clustering'])
    useRecommender         = json.loads(request.json['recommender'])
    # 10, 25, 50, 100
    numResults = int(request.json['results'])
    # the query string
    query = request.json['query']
    # query type (0 = query, 1 = suggestion)
    querytype = int(request.json['type'])

    results = []
    if querytype == 0:
        for (pmid, score) in searches.query(query, config.SUBSET, useIndependentFeatures, usePagerank, useTFIDF, useClustering, useRecommender, numResults):
            print "PubmedID: %d Scored: %f" % (pmid, score)
            print "Title: %r" % datasets.SUMMARIES[pmid].title
            results.append({'pmid': pmid, 'score':score,'title':datasets.SUMMARIES[pmid].title})
    elif querytype == 1:
        for (pmid, score) in searches.suggest(query, config.SUBSET, useIndependentFeatures, usePagerank, useTFIDF, useClustering, useRecommender, numResults):
            print "PubmedID: %d Scored: %f" % (pmid, score)
            print "Title: %r" % datasets.SUMMARIES[pmid].title
            results.append({'pmid': pmid, 'score':score,'title':datasets.SUMMARIES[pmid].title})

    return jsonify(results=results)



if __name__ == '__main__':
    # use_reloader=False will have fastest loading and smallest mem footprint (reloader uses 2 processes both having all datasets loaded.)
    app.run(debug=config.debug,use_reloader=config.use_reloader)