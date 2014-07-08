from service import Service
import textwrap
from exporter import Exporter

CMDExporter = Exporter("CMD")
cmd_exporter = CMDExporter.exporter

def takes_full_message(f):
    f._takes_full_message = True
    return f

class CMDService(Service):
    @classmethod
    def is_handler(cls, v):
        return hasattr(v, "_handles_command")
    @classmethod
    def can_handle(cls, handler, message):
        return message[0].lower() == handler._handles_command
    @classmethod
    def handler(cls, word):
        word = word.lower()
        def decorator(f):
            f._handles_command = word
            return f
        return decorator
    @classmethod
    def run(cls, handler, source, message):
        if hasattr(handler, "_takes_full_message"):
            return handler(source.get_common_state(), message)
        else:
            message = message.split()
            return handler(source.get_common_state(), *message)
    @classmethod
    def tag(cls, handler):
        return handler._handles_command

cmd_handler = CMDService.handler
