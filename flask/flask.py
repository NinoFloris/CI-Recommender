from flask import Flask
from flask import render_template, request, jsonify

app = Flask(__name__)
app.debug = True

@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    query = request.json['query']
    # do something with the query here; main recommending function

    # return a list of recommended papers with e.g. scores and stuff
    return jsonify({"query" : query})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()