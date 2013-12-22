import os

### Config ###
# Global subset for given (by professor) datasets, this way no large sets will get loaded (mem preservation feature)
# Set to "" for full sets
SUBSET = "20"

DATASETDIR = os.path.dirname(os.path.abspath(__file__)) + "/../datasets/"
PROCESSEDSETDIR = os.path.dirname(os.path.abspath(__file__)) + "/../datasets/processed"

# Caching, CACHE is the overriding variable for the more specific ones, this applies to all datasets in one way or another
CACHE = True
CACHEONDISK = True
CACHEINRAM = True
# All unprocessed datasets, are lazy loaded but once they are all loaded, take up about 250MB
CACHEUNPROCESSEDINRAM = True


# The amount of time, in seconds, a disk load call needs to take before being considered slow enough to cache in ram for fast retrieval on future requests.
# Up this value or disable CACHEINRAM if too much ram is consumed.
MEMOIZETIMETRESHOLD = 1


### Flask config ###
debug = True
# use_reloader=False will have fastest loading and smallest mem footprint (reloader uses 2 processes both having above datasets loaded)
use_reloader=False

