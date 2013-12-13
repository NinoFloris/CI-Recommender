import cPickle
import bz2
import os

import config
from helpers import timeRun, started


@timeRun
def load(path, tryBZ2=True):
    """Loads a pickled object.
    tryBZ2 is not recommended, extract these once and keep them in your local repo, git ignores these.

    Keyword arguments:
    path -- the path to the pickled object
    tryBZ2 -- if trybz2 is true it also searches for .bz2 files (default True)

    Returns -- unpickled object

    """
    if os.path.exists(path):
        try:
            return cPickle.load(open(path, 'rb'))
        except IOError:
            raise
    elif tryBZ2 and os.path.exists(path + '.bz2'):
        try:
            return cPickle.load(bz2.BZ2File(path + '.bz2', 'rb'))
        except IOError:
            raise

@started
@timeRun
def loadAll(folder, tryBZ2=True):
    """Loads a folder of pickled objects.
    tryBZ2 is not recommended, extract these once and keep them in your local repo, git ignores these.

    Keyword arguments:
    folder -- the folder to the pickled objects
    tryBZ2 --  if tryBZ2 is true it also searches for .bz2 files (default True)

    Returns -- dict: {name: unpickled object}

    """
    if os.path.exists(folder):
        datasets = {}
        bz2paths = []
        # created arrays for pkl and bz2, this way we have all the files ending with .pkl or .bz2 in 2 arrays but stripped of .bz2
        if tryBZ2:
            bz2paths = [fpath[:-4] for fpath in os.listdir(folder) if fpath.endswith('.bz2')]
        pklpaths = [fpath for fpath in os.listdir(folder) if fpath.endswith('.pkl')]
        #now merge those 2 arrays to one and create a set out of them, this way we have all the datasets, compressed or not.
        #then just first try if the .pkl variant exists, if not go for the .bz2
        for fpath in set(bz2paths + pklpaths):
            path = folder + '/' + fpath
            datasets[fpath[:-4]] = load(path)
        return datasets

@timeRun
def addToConfig(nameDataDict):
    """Lazy method of mine, uses the hidden dict of any object to add the object by string name to the variable."""
    if nameDataDict is not None:
        for name, data in nameDataDict.iteritems():
            config.__dict__[name.upper()] = data