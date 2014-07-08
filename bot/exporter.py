def Exporter(prefix):
    exporters = set()
    class _Exporter(object):
        def __init__(self, t):
            self.exptype = t
        @classmethod
        def from_module(cls, mod):
            return cls.load_all(mod).next()
        @classmethod
        def load_all(cls, mod):
            for name in dir(mod): # Should I use .__dict__?
                value = getattr(mod, name)
                if cls.is_exporter(value):
                    yield cls.load(value)
        @classmethod
        def load(cls, exp):
            return exp()
        @classmethod
        def exporter(cls, t):
            """
            Decorator marking the passed type as an exporter for this Exporter
            type.
            """
            exporters.add(id(t))
            return t
        @classmethod
        def is_exporter(cls, exp):
            return id(exp) in exporters
    _Exporter.__name__ = "%sExporter" % prefix
    return _Exporter    
