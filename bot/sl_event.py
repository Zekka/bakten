from util import memoize
from System import EventHandler
from functools import wraps
from exporter import Exporter
from service import Service

SLExporter = Exporter("sl")
sl_exporter = SLExporter.exporter

class EventTable(object):
    def __init__(self, events):
        self.events = events
    @memoize
    def responder_for(self, owner):
        """
        Returns a Responder that can work with all events that a given object
        is eligible for.

        Determines eligibility based on the object's type: if the object is an
        instance of an event's designated owner type, that event is included.

        If called with the same owner, this method should return the same
        responder. Responders contain very little state, and using multiple
        responders for the same object shouldn't break anything, though.

        You can call either this or the module-level responder_for.
        """
        return Responder(owner, filter(
            lambda x: isinstance(owner, x[0]), self.events))

class Responder(object):
    """
    Pythonic wrapper for C#'s somewhat ugly Event system.

    Use responder_for(obj) to create a Responder for an object, and then
    register(eventname, response) of that Responder to register a callback for
    the event.
    """
    def __init__(self, owner, events):
        self.events = dict(i[1:] for i in events)
            # Entries will look like {"Disconnected: DisconnectedEventArgs},
            # {"EventQueueRunning": EventQueueRunningArgs} in this case.
        self.owner = owner
        self.common_state = None
    def register(self, name, response):
        """
        Passed an event by name, and the response function, the Responder
        will automatically generate and add an event handler to its C#-style
        owner object.
        """
        if name not in self.event_names:
            raise ValueError("event not found: %s" % name)
        else:
            evtype = self.events[name]
        target = getattr(self.owner, name)
        target += EventHandler[evtype](lambda *args, **kwargs:
                response(self.common_state, *args, **kwargs)) # Pass targets our common state.
    def set_common_state(self, st):
        self.common_state = st
    @property
    @memoize
    def event_names(self):
        return self.events.keys()
    def add_module(self, mod):
        """
        Shorthand to load all Exporters from a module and add them to the
        current Responder instance.
        """
        for i in SLExporter.load_all(mod):
            i.add_to(self)

class SLService(Service):
    """
    A pseudoservice whose handlers are fed into a Responder as quickly as
    possible.
    """
    @classmethod
    def handler(cls, t):
        def decorator(f):
            f._handles_evt = t
            return f
        return decorator
    @classmethod
    def tag(cls, handler):
        return handler._handles_evt
    @classmethod
    def can_handle(cls, service, message):
        """
        This Service should never actually be used as a Service - only to add
        things to a Responder. So we don't need to determine this ever.
        """
        return NotImplemented
    @classmethod
    def is_handler(cls, v):
        return hasattr(v, "_handles_evt")
    def add_to(self, responder):
        for func in self.list_handlers():
            try:
                responder.register(type(self).tag(func), func)
            except ValueError, e:
                # Swallow this. We know we're the wrong type and will be
                # fortunately ignored.
                pass

sl_handler = SLService.handler
