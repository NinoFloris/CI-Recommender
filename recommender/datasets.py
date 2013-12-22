"""datasets.py is dedicated to hosting non processed datasets, this includes custom sets that don't have to be processed and course material datasets."""
import sys
from collections import namedtuple

import config
from dataloader import loadDataset
from helpers import sliceDict


class _Sneaky(object):
    """Class is used to fake a module, this way we can have a lazy-loading 'module'.
    Each of the properties here are a dataset that gets loaded on first call of the property function.
    """
    def __init__(self,name):
        self.module = sys.modules[name]
        sys.modules[name] = self
        self.initializing = True

        # Given datasets
        self._summaries = None
        self._citations = None
        self._ids = None
        self._abstracts = None
        self._keywords = None

        # Custom datasets
        self._stopwords = None

    @property
    def SUMMARIES(self):
        result = self._summaries
        if result is None:
            result = sliceDict(loadDataset('summaries'), config.SUBSET)
            paper = namedtuple('paper', ['title', 'authors', 'year', 'doi'])
            for (pmid, paper_info) in result.iteritems():
                result[pmid] = paper( *paper_info )

        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._summaries = result

        return result

    @property
    def CITATIONS(self):
        result = self._citations
        if result is None:
            result = sliceDict(loadDataset('citations'), config.SUBSET)
        
        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._citations = result

        return result

    @property
    def IDS(self):
        result = self._ids
        if result is None:
            result = [pmid for pmid in loadDataset('ids') if str(pmid).startswith(config.SUBSET)]

        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._ids = result
            
        return result

    @property
    def ABSTRACTS(self):
        result = self._abstracts
        if result is None:
            result = sliceDict(loadDataset('abstracts'), config.SUBSET)
        
        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._abstracts = result

        return result

    @property
    def KEYWORDS(self):
        result = self._keywords
        if result is None:
            result = sliceDict(loadDataset('keywords'), config.SUBSET)

        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._keywords = result

        return result

    @property
    def STOPWORDS(self):
        result = self._stopwords
        if result is None:
            result = loadDataset('stopwords')

        if config.CACHEUNPROCESSEDINRAM and config.CACHE:
            self._stopwords = result
            
        return result

    def __getattr__(self, name):
        # Call module.__init__ after import introspection is done
        if self.initializing and not name[:2] == '__' == name[-2:]:
            self.initializing = False
            __init__(self.module)
        return getattr(self.module, name)

def __init__(module):
    # Method for solving circular reference when modules that import datasets.py are needed in datasets.py (due to using an instance)
    # Not required at the moment, here for reference.
    pass

# Creating the object
_Sneaky(__name__)