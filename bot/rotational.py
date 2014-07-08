import threading
class Rotational(dict):
    def __init__(self, prefix):
        self.ticker = 0
        self.lock = threading.Lock()
        self.prefix = prefix
        self.reverse_lookup = {}
    def _next(self):
        with self.lock:
            self.ticker += 1
            self.ticker %= 0x10000
            return "{0}{1:04x}".format(self.prefix, self.ticker).upper()
    def __setitem__(self, k, v):
        k = k.lower()
        previous_value = self[k] if k in self else None
        dict.__setitem__(self, k, v)
        if previous_value and id(previous_value) in self.reverse_lookup:
            del self.reverse_lookup[id(previous_value)]
        self.reverse_lookup[id(v)] = k
    def __delitem__(self, k):
        v = self[k] 
        dict.__delitem__(self, k)
        if id(v) in self.reverse_lookup: del self.reverse_lookup[id(v)]
    def __getitem__(self, k):
        k = k.lower()
        return dict.__getitem__(self, k)
    def add(self, obj):
        if id(obj) in self.reverse_lookup:
            return self.reverse_lookup[id(obj)]
        name = self._next()
        self[name] = obj
        self.reverse_lookup[id(obj)] = name
        return name
