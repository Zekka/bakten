from ..service import Service
class IRCService(Service):
    @classmethod
    def is_handler(cls, v):
        return hasattr(v, "_handles_type")
    @classmethod
    def can_handle(cls, service, message):
        return isinstance(message, cls.tag(service))
    @classmethod
    def handler(cls, t):
        def decorator(f):
            f._handles_type = t
            return f
        return decorator
    @classmethod
    def tag(cls, handler):
        return handler._handles_type
irc_handler = IRCService.handler
