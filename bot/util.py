from functools import wraps
from collections import Iterable
def to_ids(o):
    # Slightly hackish method to turn unhashable things into ids
    if hasattr(o, "__hash__"):
        return hash(o)
    elif isinstance(o, Iterable):
        return tuple(map(to_ids, o))
    else:
        return id(o)

def memoize(f):
    storage = {}
    @wraps(f)
    def _f(*args, **kwargs):
        key = to_ids((tuple(args), tuple(kwargs)))
        if key not in storage:
            storage[key] = f(*args, **kwargs)
        return storage[key]
    return _f



