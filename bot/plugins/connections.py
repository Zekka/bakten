"""
Deals with connections and disconnections.
"""
from sl_event import sl_handler, sl_exporter, SLService
import OpenMetaverse
from cmd_event import cmd_handler, cmd_exporter, CMDService
from config import *
import threading
import sl

@cmd_exporter
class SLSessionCommands(CMDService):
    def __init__(self):
        self.session = None
    @cmd_handler("connect")
    def connect(self, state):
        """
        CONNECT
        Connects to game.
        """
        if self.session:
            state["irc"].error("You are already connected!")
            return
        self.session = sl.Session(state["irc"])
        g = threading.Thread(target = self.session.start)
        g.start()
    @cmd_handler("disconnect")
    def disconnect(self, state):
        """
        DISCONNECT
        Disconnects from game.
        """
        if not self.session:
            state["irc"].error("You are not connected.")
            return
        self.session.stop()
        self.session = None

@sl_exporter
class ConnectionsHandler(SLService):
    @sl_handler("LoginProgress")
    def on_login(self, state, sender, args):
        if args.Status == OpenMetaverse.LoginStatus.ConnectingToLogin:
            state["irc"].status("Beginning login.")
        elif args.Status == OpenMetaverse.LoginStatus.Success:
            state["irc"].status("Login succeeded.")
        elif args.Status == OpenMetaverse.LoginStatus.Failed:
            state["irc"].status("Login failed: %s" % args.FailReason)
    @sl_handler("SimConnecting")
    def on_sim_connecting(self, state, sender, args):
        sim = args.Simulator
        state["irc"].status("Connecting: %s" % sim)
    @sl_handler("SimConnected")
    def on_sim_connected(self, state, sender, args):
        sim = args.Simulator
        state["irc"].status("Connected: %s" % sim)
    @sl_handler("SimDisconnected")
    def on_sim_disconnected(self, state, sender, args):
        sim = args.Simulator
        state["irc"].status("Disconnected: %s" % sim)
