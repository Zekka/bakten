from service import IRCService, irc_handler
from messages import *
class IRCRules(IRCService):
    @irc_handler(JustConnected)
    def register(self, ircclient, _):
        msgs = []
        if ircclient.cfgget("pass"):
            g = PassMessage.create()
            g["pass"] = ircclient.cfgget("pass")
            msgs.append(g)
        n = NickMessage.create()
        n["nickname"] = ircclient.cfgget("nick")
        msgs.append(n)
        u = UserMessage.create()
        u["user"] = ircclient.cfgget("user")
        u["realname"] = ircclient.cfgget("realname")
        msgs.append(u)
        ircclient.sendmany(msgs)
    @irc_handler(PingMessage)
    def handle_ping(self, ircclient, message):
        pong = PongMessage(message.args)
        ircclient.send(pong)
    @irc_handler(PrivmsgMessage)
    def handle_ctcp(self, ircclient, message):
        text = message["text"]
        if text[0] != "\x01":
            return
        body = text[1:-1].strip()
        if body.upper() == "VERSION":
            p = PrivmsgMessage.create()
            p["text"] = irclient.cfgget("version", "bakten.irc")
            p["user"] = message.source
            ircclient.send(p)

"""
Useful templates for other services.
"""
class ActAfterWelcome(IRCService):
    @irc_handler(WelcomeReply)
    def _act(self, ircclient, message):
        self.act(ircclient, message)

class ActBeforeLeave(IRCService):
    @irc_handler(AboutToLeave)
    def _act(self, ircclient, message):
        self.act(ircclient, message)
