from time import time

def slicedict(d, s):
    return {k:v for k,v in d.iteritems() if k.startswith(s)}

def transformDict(data):
    result={}
    for key in data:
        for val in data[key]:
            result.setdefault(val,{})
            # Flip author and title
            result[val][key] = 0.0
    return result

def timeRun(func, *args):
    t0 = time()
    ret = func(*args)
    t1 = time()
    return (t1 - t0, ret)
