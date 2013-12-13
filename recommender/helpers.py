import time
import cPickle
import inspect
# using decorator to keep function metadata intact, this way multiple decorators with f.func_name are possible
from external.decorator import decorator

def slicedict(d, s):
    return {k:v for k,v in d.iteritems() if k.startswith(s)}

def pickleObject(obj, path):
    cPickle.dump(obj, open(path, 'wb'), cPickle.HIGHEST_PROTOCOL)

@decorator
def timeRun(f, *args):
    time1 = time.time()
    ret = f(*args)
    time2 = time.time()

    print '"%s" function finished its work in %fs' % (f.__module__ + '->' + f.__name__, (time2-time1))
    return ret

@decorator
def started(f, *args):
    print '"%s" function started its work' % (f.__module__ + '->' + f.__name__)
    return f(*args)