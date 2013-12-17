import time
import cPickle
import bz2
# using decorator to keep function metadata intact, this way multiple decorators with f.func_name are possible
from external.decorator import decorator


def sliceDict(d, sliceOn, key=lambda key, value: key):
    """Slices a dict.

    Keyword arguments:
    d -- the dictionary to slice
    sliceOn -- what to slice on, will be converted to string
    key -- like the sorted() key argument, pas a lambda with arguments key value and return the element to compare with

    Returns -- dict: {k: v}

    """
    if sliceOn:
        return {k: v for k, v in d.iteritems() if str(key(k, v)).startswith(str(sliceOn))}

    return d

def pickleObject(obj, path, asBZ2=False):
    if asBZ2:
        cPickle.dump(obj, bz2.BZ2File(path, 'wb'), cPickle.HIGHEST_PROTOCOL)
    else:
        cPickle.dump(obj, open(path, 'wb'), cPickle.HIGHEST_PROTOCOL)

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

    print '"%s" function returned %d elements' % (f.__module__ + '->' + f.__name__, len(ret))
    return ret

