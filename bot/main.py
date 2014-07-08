from irc import IRCClient
from irc.services import ActAfterWelcome
from irc.service import IRCService, irc_handler
from irc.messages import *
from config import *
import textwrap
import sl
import sys
import threading
import System
import decision
import plugin
import traceback
from cmd_event import CMDExporter, CMDService

class Bakten(IRCClient):
    def __init__(self, *args, **kwargs):
        IRCClient.__init__(self, *args, **kwargs)

        self.decision_table = {}
        self.decision_ticker = 0
        self.decision_lock = threading.Lock()
    def services(self):
        yield AutojoinChannel(IRC_CHANNEL, IRC_KEY)
        yield BaktenCommandService()
        yield decision.DecisionService(self)
    def error(self, msg):
        self.status("ERROR: %s" % msg)
    def status(self, msg):
        pmsg = PrivmsgMessage.create()
        pmsg["target"] = IRC_CHANNEL
        pmsg["text"] = "== {0}".format(msg)
        self.send(pmsg)

class AutojoinChannel(ActAfterWelcome):
    def __init__(self, chan, key):
        self.msg = JoinMessage([chan, key])
    def act(self, ircclient, message):
        ircclient.send(self.msg)

class BaktenCommandService(IRCService):
    def __init__(self):
        self.services = []
        for i in plugin.find_plugins(PLUGIN_DIR):
            self.services.extend(
                CMDExporter.load_all(i)
                )
        print self.services
    def patch(self, ircclient):
        ircclient.doc_cmd = self.doc_cmd
        ircclient.list_commands = self.list_commands
        for i in self.services:
            i.patch(ircclient)
    @irc_handler(PrivmsgMessage)
    def check_cmd(self, ircclient, message):
        msg = message["text"]
        if not msg.startswith(COMMAND_PREFIX): return
        cmd, _, args = msg[len(COMMAND_PREFIX):].strip().partition(" ")
        cmd = cmd.lower()
        try:
            cmdfunc = self.find_cmd(cmd)
        except ValueError:
            ircclient.error("No such command: %s." % cmd)
            return
        try:
            CMDService.run(cmdfunc, ircclient, args)
        except TypeError, e:
            ircclient.error("Incorrect number of arguments: %s." % cmd)
            ircclient.error("This might also be a TypeError: %s." % e)
            traceback.print_exc()
            return
        except Exception, e:
            traceback.print_exc()
            ircclient.error("Command failed: %s, %s." % (type(e), e))
    def find_cmd(self, name):
        name = name.lower()
        for i in self.services:
            handler = i.find_handler(name)
            if handler:
                return handler
        raise ValueError("Not a command: %s" % name)
    def doc_cmd(self, name):
        cmd = self.find_cmd(name)
        nodoc = "No documentation for %s." % name
        if not cmd: return nodoc
        doc = cmd.__doc__
        if not doc: return nodoc
        return textwrap.dedent(doc).strip()
    def list_commands(self):
        """
        Returns the name of each command available to the BaktenCommandService.
        """
        for i in self.services:
            for cmd in i.list_handlers():
                yield type(i).tag(cmd)

def main():    
    b = Bakten(host=IRC_SERVER, nick=IRC_NICK)
    b.loop()

if __name__ == "__main__":
    main()
