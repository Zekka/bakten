from cmd_event import *

@cmd_exporter
class IRCHelpService(CMDService):
    @cmd_handler("help")
    def help(self, state, command = None):
        """
        HELP [command]
        Displays help on a given command, or else displays a list of commands.
        Use LIST alternately to list all commands.
        """
        if not command:
            self.list_(state)
            return
        state["irc"].add_lines(state, state["irc"].doc_cmd(command).split("\n"))
    @cmd_handler("list")
    def list_(self, state):
        """
        LIST
        Lists all commands.
        """
        state["irc"].add_lines(state,
            ("\n \n".join(map(state["irc"].doc_cmd,
             state["irc"].list_commands())).split("\n"))
            )
            # The split() and join() are there so that the newlines in
            # command documentation are removed.
            
