import cPickle
import bz2
import os

import config
from helpers import printTimeRun, printStarted, printSetSize, pickleObject, memoize


@printSetSize
@printTimeRun
@memoize
def load(path, unpackBZ2=True, loadBZ2=False):
    """Loads a pickled object.
    only use loadBZ2 when disk space is limited, much slower unpacked '.pkl' files.
    path gets priority above unpackBZ2 and that gets priority above loadBZ2.


    Keyword arguments:
    path -- (str) path to pickled object
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)

    Returns -- unpickled_object

    """
    try:
        if os.path.exists(path):
            with open(path, 'rb') as pickle:
                return cPickle.load(pickle)
        elif unpackBZ2 and os.path.exists(path + '.bz2'):
            with bz2.BZ2File(path + '.bz2', 'rb') as f:
                unpacked = f.read()
                with open(path, 'wb') as pkl:
                    pkl.write(unpacked)
                return cPickle.loads(unpacked)
        elif loadBZ2 and os.path.exists(path + '.bz2'):
            with bz2.BZ2File(path + '.bz2', 'rb') as pickle:
                return cPickle.load(pickle)
    except IOError:
        raise

@printStarted
@printTimeRun
def loadAll(folder=os.path.dirname(__file__) + "/../datasets/", unpackBZ2=True, loadBZ2=False):
    """Loads a folder of pickled objects.
    only use loadBZ2 when disk space is limited, much slower unpacked '.pkl' files.
    '*.pkl' files get priority above unpackBZ2 and that gets priority above loadBZ2.

    Keyword arguments:
    folder -- (str) folder to pickled objects (default thisdir/../datasets/)
    unpackBZ2 -- (bool) if '*.pkl' not found, looks in folder for '*.pkl.bz2' unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if '*.pkl' not found, looks in folder for '*.pkl.bz2' then loads that (default False)

    Returns -- dict: {name: unpickled_object}

    """
    if os.path.exists(folder):
        datasets = {}
        bz2paths = []
        # created arrays for pkl and bz2, this way we have all the files ending with .pkl or .bz2 in 2 arrays but stripped of .bz2
        if unpackBZ2 or loadBZ2:
            bz2paths = [fpath[:-4] for fpath in os.listdir(folder) if fpath.endswith('.bz2')]
        pklpaths = [fpath for fpath in os.listdir(folder) if fpath.endswith('.pkl')]
        #now merge those 2 arrays to one and create a set out of them, this way we have all the datasets, compressed or not.
        #then just first try if the .pkl variant exists, if not go for the .bz2
        for fpath in set(bz2paths + pklpaths):
            path = folder + '/' + fpath
            datasets[fpath[:-4]] = load(path, unpackBZ2, loadBZ2)
        return datasets

@printTimeRun
def addToConfig(nameDataDict):
    """Lazy method of mine, uses the hidden dict of any object to add the object by string name to the variable.

    Keyword arguments:
    nameDataDict -- (dict) the names and their objects to add to the config file

    Returns -- None

    """
    if nameDataDict is not None:
        for name, data in nameDataDict.iteritems():
            config.__dict__[name.upper()] = data


def loadProcessed(keyName, setName, subSet, path=os.path.dirname(__file__) + "/../datasets/processed/", unpackBZ2=True, loadBZ2=False):
    """Loads a processed object with a specific naming scheme.

    Keyword arguments:
    keyName -- (str) key to the object, this can be a function name or a description
    setName -- (str) descriptive name of the data in the object
    subSet -- (str) any subset created from an original, used to find slices
    path -- (str) path of the folder to save in (default thisdir/../datasets/processed/))
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)

    Returns -- unpickled processed object

    """
    #this could be numeric like 20 or None
    subSet = str(subSet)
    obj = None
    #example: path_to_datasets/TFIDF_abstracts_20.pkl
    fPath = path + '/' + keyName + '_' + setName + '_' + subSet +  '.pkl'

    if os.path.exists(fPath) or (unpackBZ2 or loadBZ2) and os.path.exists(fPath + '.bz2'):
        obj = load(fPath, unpackBZ2, loadBZ2)

    return obj

def saveProcessed(procObj, keyName, setName, subSet, path=os.path.dirname(__file__) + "/../datasets/processed/", saveBZ2=False):
    """Saves a processed object with a specific naming scheme.

    Keyword arguments:
    procObj -- (object) any object to be saved
    keyName -- (str) key for the object, this can be a function name or a description
    setName -- (str) descriptive name of the data in the object
    subSet -- (str) any subset created from an original, used to find slices
    path -- (str) path of the folder to save in (default thisdir/../datasets/processed/))
    saveBZ2 -- (bool) if it should also save a BZ2 compressed '.pkl.bz2' file along with the uncompressed'.pkl' file

    Returns -- unpickled processed object

    """
    #this could be numeric like 20 or None
    subSet = str(subSet)
    #example: path_to_datasets/TFIDF_abstracts_20.pkl
    fPath = path + '/' + keyName + '_' + setName + '_' + subSet +  '.pkl'

    #check if folders resolve to an existing path
    if os.path.exists(path):
        pickleObject(procObj, fPath)
        if saveBZ2:
            pickleObject(procObj, fPath + '.bz2', True)
        return procObj
