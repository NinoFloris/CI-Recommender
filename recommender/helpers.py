import time
import cPickle
import bz2
# using decorator to keep function metadata intact, this way multiple decorators with f.func_name are possible
from external.decorator import decorator
import operator

@decorator
def printTimeRun(f, *args):
    time1 = time.time()
    ret = f(*args)
    time2 = time.time()

    print '"%s" function finished its work in %fs' % (f.__module__ + '->' + f.__name__, (time2-time1))
    return ret

@decorator
def printStarted(f, *args):
    print '"%s" function started its work' % (f.__module__ + '->' + f.__name__)
    return f(*args)

@decorator
def printSetSize(f, *args):
    ret = f(*args)
    length = None
    if ret is not None:
        length = len(ret)

    print '"%s" function returned %r elements' % (f.__module__ + '->' + f.__name__, length)
    return ret

@decorator
def mockReturnNone(f, *args):
    f(*args)

    print '"%s" function mocked to return None' % (f.__module__ + '->' + f.__name__)
    return None

@decorator
def memoize(f, *args, **kw):
    if kw: # frozenset is used to ensure hashability
        key = args, frozenset(kw.iteritems())
    else:
        key = args
        cache =  f.__dict__.setdefault('cache', {}) # attributed added by memoize
    if key in cache:
        return cache[key]
    else:
        result = f(*args, **kw)
        cache[key] = result
        return result

@printTimeRun
def normalizeScore(sortedList):
    """Normalizes score from 0 to 1 based on the highest score found, modifies given list.

    Keyword arguments:
    sortedList -- (list) this function accepts a sorted list with descending scores in the format [(pmid, score)]

    returns -- sortedList with normalized scores: [(pmid, score)]
    """
    if len(sortedList) == 0:
        return

    highest = sortedList[0][1] 

    if highest == 0:
        return

    # not using list comprehension but updating list to preserve memory
    for i, (pmid, score) in enumerate(sortedList):
        sortedList[i] = (pmid, score/highest)

def pickleObject(obj, path, asBZ2=False):
    if asBZ2:
        cPickle.dump(obj, bz2.BZ2File(path, 'wb'), cPickle.HIGHEST_PROTOCOL)
    else:
        cPickle.dump(obj, open(path, 'wb'), cPickle.HIGHEST_PROTOCOL)

@printTimeRun
@printSetSize
def sliceDict(d, sliceOn, key=operator.itemgetter(0)):
    """Slices a dict.

    Keyword arguments:
    d -- the dictionary to slice
    sliceOn -- what to slice on, will be converted to string
    key -- like the key in sorted(), tuple input to a lambda or itemgetter return element to compare with, will be converted to string for startswith match

    Returns -- dict: {k: v}

    """
    if sliceOn:
        sliceOn = str(sliceOn)
        return {k: v for k, v in d.iteritems() if str(key((k, v))).startswith(sliceOn)}

    return d

class CachedProperty(object):
    """Lazy-loading read/write property descriptor.
    Value is stored locally in descriptor object. If value is not set when
    accessed, value is computed using given function. Value can be cleared
    by calling 'del'.
    """

    def __init__(self, func):
        self._func = func
        self._values = {}
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        if obj not in self._values or self._values[obj] is None:
            self._values[obj] = self._func(obj)
        return self._values[obj]

    def __set__(self, obj, value):
        self._values[obj] = value

    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]
        self._values[obj] = None
