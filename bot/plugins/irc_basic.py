"""
Basic commands for IRC.
"""
from cmd_event import cmd_handler, cmd_exporter, CMDService
from config import *
import System.Environment

@cmd_exporter
class IRCBasicCommands(CMDService):
    @cmd_handler("quit")
    def quit(self, state):
        """
        QUIT
        Quits from IRC.
        """
        state["irc"].quit(QUIT_MESSAGE)
        System.Environment.Exit(0)

