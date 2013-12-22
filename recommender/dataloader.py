import cPickle
import bz2
import os
import time

import config
from helpers import printTimeRun, printSetSize, pickleObject, printStarted


@printSetSize
@printTimeRun
def load(path, unpackBZ2=True, loadBZ2=False):
    """Loads a pickled object.
    Only use loadBZ2 when disk space is limited, much slower than unpacked '.pkl' files.
    path will first be tried, then unpackBZ2 and only then loadBZ2.

    Keyword arguments:
    path -- (str) path to pickled object.
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)

    Returns -- unpickled object

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

def loadDataset(setName, folder=config.DATASETDIR, unpackBZ2=True, loadBZ2=False):
    """Loads a pickled object, with setName + .pkl from folder.
    Only use loadBZ2 when disk space is limited, much slower than unpacked '.pkl' files.
    path will first be tried, then unpackBZ2 and only then loadBZ2.

    Keyword arguments:
    setName -- (str) descriptive name of the data in the object.
    folder -- (str) folder to pickled object (default is config.DATASETDIR).
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)

    Returns -- unpickled object

    """
    return load(folder.rstrip('/') + '/' + setName + '.pkl', unpackBZ2, loadBZ2)

@printTimeRun
def memoizedLoad(setName, folder=config.DATASETDIR, unpackBZ2=True, loadBZ2=False, memoizeTimeTresh=config.MEMOIZETIMETRESHOLD):
    """Loads a pickled object, with setName + .pkl from folder or if memoized from cache.
    Only use loadBZ2 when disk space is limited, much slower than unpacked '.pkl' files.
    path gets priority above unpackBZ2 and that gets priority above loadBZ2.

    Keyword arguments:
    setName -- (str) descriptive name of the data in the object.
    folder -- (str) folder to pickled object (default is config.DATASETDIR).
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)
    memoizeTimeTresh -- (int) amount of seconds loading required before result will be cached.

    Returns -- unpickled object

    """
    result = None

    # Create key for cache 
    key = (setName, folder)

    # Try to get the cache
    cache = memoizedLoad.__dict__.setdefault('cache', {}) # attributed added by memoize

    # Path has been loaded before? return.
    if key in cache:
        result = cache[key]
    else:
        time1 = time.time()
        if config.CACHEONDISK and config.CACHE:
            result = loadDataset(setName, folder, unpackBZ2, loadBZ2)
        time2 = time.time()

        # If ram caching is allowed and treshold is reached, cache to ram, if disk caching is allowed and ram caching not, return from disk
        if time2 - time1 >= memoizeTimeTresh and config.CACHEINRAM and config.CACHE:
            cache[key] = result
        # Going around the time treshold here because there can be made no disk loads at all to time, just cache it.
        elif config.CACHEINRAM and not config.CACHEONDISK and config.CACHE:
            cache[key] = result

    return result

def loadProcessed(keyName, setName, subSet, folder=config.PROCESSEDSETDIR, unpackBZ2=True, loadBZ2=False):
    """Loads a processed object with a specific naming scheme.
    Results (if processing is longer than 1 sec) are cached through the use of the memoize decorator.

    Keyword arguments:
    keyName -- (str) key to the object, this can be a function name or a description
    setName -- (str) descriptive name of the data in the object
    subSet -- (str) any subset created from an original, used to find slices
    folder -- (str) path of the folder to save in (default thisdir/../datasets/processed/))
    unpackBZ2 -- (bool) if path not found looks for 'path + .bz2', unpacks it then loads unpacked (default True)
    loadBZ2 -- (bool) if path not found looks for 'path + .bz2' then loads that (default False)

    Returns -- unpickled processed object

    """
    # This could be numeric like 20 or None
    subSet = str(subSet)
    if not subSet:
        subSet = config.SUBSET
    obj = None
    # Example: path_to_datasets/TFIDF_abstracts_20.pkl
    fPath = folder + '/' + keyName + '_' + setName + '_' + subSet +  '.pkl'
    key = keyName + '_' + setName + '_' + subSet
        
    if os.path.exists(fPath) or (unpackBZ2 or loadBZ2) and os.path.exists(fPath + '.bz2'):
        obj = memoizedLoad(key, folder, unpackBZ2, loadBZ2)

    return obj

def saveProcessed(procObj, keyName, setName, subSet, folder=config.PROCESSEDSETDIR, saveBZ2=False):
    """Saves a processed object with a specific naming scheme.

    Keyword arguments:
    procObj -- (object) any object to be saved
    keyName -- (str) key for the object, this can be a function name or a description
    setName -- (str) descriptive name of the data in the object
    subSet -- (str) any subset created from an original, used to find slices
    folder -- (str) path of the folder to save in (default thisdir/../datasets/processed/))
    saveBZ2 -- (bool) if it should also save a BZ2 compressed '.pkl.bz2' file along with the uncompressed'.pkl' file

    Returns -- unpickled processed object

    """
    # This could be numeric like 20 or None
    subSet = str(subSet)
    if not subSet:
        subSet = config.SUBSET
    # Example: path_to_datasets/TFIDF_abstracts_20.pkl
    fPath = folder.rstrip('/') + '/' + keyName + '_' + setName + '_' + subSet +  '.pkl'
    key = keyName + '_' + setName + '_' + subSet 
    key = (key, folder)

    # Feels kind of hacky, but is required to make exclusive in ram caching possible
    if config.CACHEINRAM and config.CACHE:
        memoizedLoad.__dict__.setdefault('cache', {})[key] = procObj

    # Check if folders resolve to an existing path
    if os.path.exists(folder) and config.CACHEONDISK and config.CACHE:
        pickleObject(procObj, fPath)
        if saveBZ2:
            pickleObject(procObj, fPath + '.bz2', True)
        return procObj


# Deprecated in favor of datasets.py
@printStarted
@printTimeRun
def loadAll(folder=config.DATASETDIR, unpackBZ2=True, loadBZ2=False, lazily=True, loadClass=False):
    """Loads a folder of pickled objects.
    Only use loadBZ2 when disk space is limited, much slower than unpacked '.pkl' files.
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
        # Created arrays for pkl and bz2, this way we have all the files ending with .pkl or .bz2 in 2 arrays but stripped of .bz2
        if unpackBZ2 or loadBZ2:
            bz2paths = [fpath[:-4] for fpath in os.listdir(folder) if fpath.endswith('.bz2')]
        pklpaths = [fpath for fpath in os.listdir(folder) if fpath.endswith('.pkl')]
        # Now merge those 2 arrays to one and create a set out of them, this way we have all the datasets, compressed or not.
        # Then just first try if the .pkl variant exists, if not go for the .bz2
        for fpath in set(bz2paths + pklpaths):
            path = folder + '/' + fpath
            datasets[fpath[:-4]] = load(path, unpackBZ2, loadBZ2)
        return datasets

# Deprecated in favor of datasets.py
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
