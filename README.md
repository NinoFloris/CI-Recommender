# Collective Intelligence Recommender
A recommender engine that makes recommendations based on papers/authors from the PubMed database.

## Usage
There are 2 ways to run our project

* Web interface
* Each module independently

For the web interface run (from inside the project dir):
```
python site.py
```

To use a module independently (from inside the project dir):
```
python
from recommender import %modulename%
%modulename%.query%ModuleName%(query(e.g. evolution virus),subSet(global subset + e.g 10),independentRun(True),topN(e.g. 100))
```

Example:
```
python
from recommender import TFIDF
TFIDF.queryTFIDF(query(e.g. "evolution virus"),subSet(global subset + e.g "10" or None),independentRun(True),topN(e.g. 100))
```


## Naming conventions
Variables, functions and parameters are pascalCased (not like PEP underscored)  
Classes are CamelCased  
Modules are lowercased unless it is an abreviation (like TFIDF)  
Config globals are UPPERCASED  

Our dataset files in "/datasets" are all subsets of "evolution" this is not mentioned in the filename.  
Raw pickle files have the extenstion: ```.pkl```  
BZ2 compressed pickle files have the extenstion: ```.pkl.bz2```  

Our processed (cached) files in "/datasets/processed" have the same extention scheme as in "/datasets".  
The naming scheme however is as follows:
```
keyName_setName_subSet
```

keyName:  
```
A specific key, a function name or a description about what changed the set e.g. normalized
```
setName:  
```
The name of the set, this can be an original set like abstracts or a new one like titles
```
subSet:  
```
States what subset this is (e.g. a subset of 20 means all the pubmed id's that start with 20).
```

## Documentation
We are using docstrings according to the PEP 257 docstring conventions.  

Example:  
```
def pageEank(paperCitations, paperCitedBy, minChanges=10, maxRounds=150):  
    """Calculates the pagerank for every citation of the papers we have citation data of.  
  
    Keyword arguments:  
    paperCitations -- (dict) dictionary containing all the papers and their citations  
    paperCitedBy -- (dict) inversed dictionary of paperCitations  
    minChanges -- (int) minimum of changes required for the loop to continue (default 10)  
    maxRounds -- (int) max rounds pagerank should do, minChanges breaks out of this loop first (default 150)  
  
    Returns -- tuple: (rounds=int, {pmid: pagerank})  
  
    """
```

I.e. starting the function with a multiline comment.  
Starting with a summary of the functionality on the same line as the quotes.  

Then explaining the different arguments in the function starting with:  
```
Keyword arguments:
```
Each argument is formatted as below:  
```
argument -- (type) description
```

The return is really code based and abstracted:  
```
Returns -- (name=string, [{k: v}])
```
The above sentence essentially says the same as:  
```
This function returns a tuple that has a name of type string and an array of dictionaries in it
```
The type is not required but if it the name doesn't really clarify what type it is then the added type is preferred.

## Commenting
When you are using domain-specific code, like a complicated calculation, please comment those lines.
Also when you feel certain lines need extra clarification, first try to see if you could maybe change the line to clearer code. 
If this is not possible please comment those lines!

Example:  
```
#return TF score per word based on the frequency of every word in tfrequency divided by tmax  
return [(f[0], float(f[1])/tmax) for f in tfrequency]  
```
As you can see, please try to refrain from using inline comments, place them above the designated line.