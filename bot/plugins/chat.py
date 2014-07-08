"""
Deals with chat.
"""
from sl_event import sl_handler, sl_exporter, SLService
from cmd_event import cmd_handler, cmd_exporter, CMDService, takes_full_message
import OpenMetaverse
from OpenMetaverse import ChatType, ChatSourceType, UUID
from System.Collections.Generic import List
from slutil.names import AvatarNames, people
from slutil.uuid import intern_uuid
chat_names_by_type = {
  # ChatType.Member         : "Member"      ,
    ChatType.Whisper        : "Whisper"     ,
    ChatType.Normal         : "Normal"      ,
    ChatType.Shout          : "Shout"       ,
    ChatType.StartTyping    : "StartTyping" ,
    ChatType.StopTyping     : "StopTyping"  ,
    ChatType.Debug          : "Debug"       ,
    ChatType.OwnerSay       : "OwnerSay"    ,
    ChatType.RegionSay      : "RegionSay"   ,
    }

chat_types_by_name_lcase = dict((v.lower(), k)
    for k, v in chat_names_by_type.items())

def figure_out_name(state, message):
    # Figures out sender name
    if message.SourceType != ChatSourceType.Agent:
        return message.FromName
    else:
        uuid = message.OwnerID
        g = AvatarNames.name_from_uuid(state, uuid)
        return ((" [%s] " % people.add(intern_uuid(uuid))) 
            + (g + " (%s)" % message.FromName if g
            else message.FromName + " (display name pending)")
            )

@sl_exporter
class ChatHandler(SLService):
    @sl_handler("ChatFromSimulator")
    def simulator_chat(self, state, sender, args):
        msgtype = chat_names_by_type[args.Type]
        name = figure_out_name(state, args)
        if msgtype == "StartTyping":
            # ircclient.status("%s has started typing." % name)
            pass
        elif msgtype == "StopTyping":
            # ircclient.status("%s has stopped typing." % name)
            pass
        else:
            message = args.Message
            state["irc"].status("[%s][%s]: %s" % (msgtype, name, message))

@cmd_exporter
class ChatCommands(CMDService):
    def __init__(self):
        self.type_ = chat_types_by_name_lcase["normal"]
    @cmd_handler("chattype")
    def chat_type(self, state, type_):
        """
        CHATTYPE newtype
        Sets the active chat type.
        Valid types are Whisper, Normal, and Shout.
        """
        type_ = type_.lower()
        if type_ not in ["whisper", "normal", "shout"]:
            state["irc"].error("Not a valid chat type.")
            return
        self.type_ = chat_types_by_name_lcase[type_]
    @takes_full_message
    @cmd_handler("say")
    def say(self, state, message):
        """
        SAY
        Says a method with the current chat type.
        Use CHATTYPE to change the current chat type. Use IM (not yet implemented) to send an IM.
        """
        state["sl"].Self.Chat(
            message, 0,
            self.type_)
