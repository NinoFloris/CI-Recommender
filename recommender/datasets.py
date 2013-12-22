"""datasets.py is dedicated to hosting non processed datasets, this includes custom sets that don't have to be processed and course material datasets."""
import sys
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
        if self._summaries is None:
            self._summaries = sliceDict(loadDataset('summaries'), config.SUBSET)
        return self._summaries

    @property
    def CITATIONS(self):
        if self._citations is None:
            self._citations = sliceDict(loadDataset('citations'), config.SUBSET)
        return self._citations

    @property
    def IDS(self):
        if self._ids is None:
            self._ids = sliceDict(loadDataset('ids'), config.SUBSET)
        return self._ids

    @property
    def ABSTRACTS(self):
        if self._abstracts is None:
            self._abstracts = sliceDict(loadDataset('abstracts'), config.SUBSET)
        return self._abstracts

    @property
    def KEYWORDS(self):
        if self._keywords is None:
            self._keywords = sliceDict(loadDataset('keywords'), config.SUBSET)
        return self._keywords

    @property
    def STOPWORDS(self):
        if self._stopwords is None:
            self._stopwords = loadDataset('stopwords')
        return self._stopwords

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