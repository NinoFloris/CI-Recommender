import unicodedata
from nltk import stem

def normalizeContent(documents, stopWords=set(), normFunction=None, stripChars=''.join(c for c in map(chr, range(32,127)) if not c.isalpha()), normalizeCase=True, removeDot=True):
    #setify our stopwords, just in case a list was passed, set is proportionally faster than list due to O(1) lookup
    stopWords = set(stopWords)
    normalized = {}
    for pmid, document in documents.iteritems():
        #replace all unicode chars with compatible ascii characters, also increases tf chance on rare words.
        document = unicodedata.normalize('NFKD', unicode(document)).encode('ascii', 'ignore')
        #split the document for easier filtering
        words = document.split()
        #removes all the stopwords and split-garbage, reuse list
        words[:] = [word.strip(stripChars) for word in words if word.lower() not in stopWords]
        if removeDot:
            words[:] = [word.replace('.', '') for word in words]

        if normalizeCase:
            words[:] = [word.lower() for word in words]

        #run external normalization function on words
        if normFunction:
            words = normFunction(words)

        #and convert it back to a string
        normalized[pmid] = ''.join(word + ' 'for word in words)[:-1]

    return normalized

def lemmatization(words):
    wnl = stem.WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in words]
