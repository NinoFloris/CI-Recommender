# Collective Intelligence Recommender
A recommender engine that makes recommendations based on papers/authors from the PubMed database.

## Documentation
We are using docstrings according to the PEP 257 docstring conventions.  

Example:  
```
def pagerank(paperCitations, paperCitedBy, minChanges=10, maxRounds=150):  
    """Calculates the pagerank for every citation of the papers we have citation data of.  
  
    Keyword arguments:  
    paperCitations -- the dict containing all the papers and their citations  
    paperCitedBy -- the inversed dict of paperCitations  
    minChanges -- the minimum of changes required for the loop to continue (default 10)  
    maxRounds -- the max rounds pagerank should do, minChanges breaks out of this loop first (default 150)  
  
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
argument -- description
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

## Usage
To be done