import unicodedata
import nltk

#globalling it because it is very slow to init
_wnl = nltk.stem.WordNetLemmatizer()
_wnl.lemmatize('warmingup')

def normalizeDocuments(documents, stopWords=set(), normFunction=None, stripChars=''.join(c for c in map(chr, range(32,127)) if not c.isalpha()), normalizeCase=True, removeDot=True):
    normalized = {}
    for pmid, document in documents.iteritems():
        normalized[pmid] = normalizeString(document, stopWords, normFunction, stripChars, normalizeCase, removeDot)

    return normalized

def normalizeString(string, stopWords=set(), normFunction=None, stripChars=''.join(c for c in map(chr, range(32,127)) if not c.isalpha()), normalizeCase=True, removeDot=True):
    #setify our stopwords, just in case a list was passed, set is proportionally faster than list due to O(1) lookup
    stopWords = set(stopWords)
    #replace all unicode chars with compatible ascii characters, also increases tf chance on rare words.
    s = unicodedata.normalize('NFKD', unicode(string)).encode('ascii', 'ignore')
    #split the document for easier filtering
    words = s.split()
    #removes all the stopwords and split-garbage, reuse list
    words[:] = [word.strip(stripChars) for word in words if word.lower() not in stopWords]
    if removeDot:
        words[:] = [word.replace('.', '') for word in words]

    if normalizeCase:
        words[:] = [word.lower() for word in words]

    #run external normalization function on words
    if normFunction:
        words = normFunction(words)

    #return and convert it back to a string
    return ''.join(word + ' 'for word in words)[:-1]


def stemming(words):
    stemmer = nltk.stem.PorterStemmer()
    return [stemmer.stem(word) for word in words]

def lemmatization(words):
    return [_wnl.lemmatize(word) for word in words]
