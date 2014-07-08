from StringIO import StringIO
import re

def read_until(buf, char): # Char is not included in the output
    cs = StringIO()
    while True:
        c = buf.read(1)
        if c == char or c == "":
            return cs.getvalue()
        cs.write(c) 

pattern = re.compile(r"[\r\n]")
def remove_newlines(s):
    return pattern.sub("", s)

message_representations = {}

def cut_at_last_value(l):
    last_value = -1
    for i in range(len(l)):
        if l[i] != None: last_value = i
    out = l[:last_value + 1]
    return out

class IRCMessage(object):
    def write(msg): # Can be called either as IRCMessage.write(msg) or msg.write()
        args = cut_at_last_value(msg.args)
        if any(i is None for i in args):
            raise ValueError("message's arguments are incoherent" +
                    " -- some optional arguments are included while their" +
                    " prerequisite arguments have not been.")
        output = StringIO()
        if msg.source:
            output.write(":")
            output.write(msg.source)
            output.write(" ")
        output.write(msg.command.upper())
        if not args: return remove_newlines(output.getvalue())
        for i in args[:-1]:
            s = str(i)
            if " " in s:
                raise ValueError("space in arg aside from final arg")
            output.write(" ")
            output.write(str(i))
        last = args[-1]
        output.write(" ")
        if " " in last:
            output.write(":")
            output.write(last)
        else:
            output.write(last)
        g = output.getvalue()
        return remove_newlines(g)
    
def parse(msg_):
    # This is really ugly, but hey, IRC is an ugly protocol.
    msg_ = msg_.strip("\r\n")
    w1_source = msg_[0] == ":"
    msg = StringIO(msg_)
    if w1_source:
        w1 = read_until(msg, " ")
        source = w1[1:]
    else:
        source = None
    command = read_until(msg, " ")
    args = []
    while True:
        arg = read_until(msg, " ")
        if arg:
            if arg[0] == ":":
                args.append(arg[1:] + " " + msg.read())
                break
            else:
                args.append(arg)
        else:
            break
    return create(command, args, source)
  
def create(command, args, source = None):
    try:
       return message_representations[command.lower()](args, source)
    except KeyError, e:
        raise UnknownMessageError("unknown message type %s" % command.lower())

class UnknownMessageError(Exception): pass

def _set_creating(list_, pos, value):
    while len(list_) < pos:
        list_[pos] = None
    list_[pos] = value

def MessageType(command, slots):
    command = command.lower()
    slot_tbl = dict((slots[pos], pos) for pos in range(len(slots)))
    class Message(IRCMessage):
        def __init__(self, args, source = None):
            if len(slots) > 0:
                if slots[-1][0] == ":": # consumes all possible args
                    args = args[:len(slots) - 1] + [
                            " ".join(args[len(slots) + 1:
                                ])]
            if len(args) > len(slots):
                raise ValueError("too many arguments for this message type")
            self.source = source
            self.args = args
            self.command = command
        def __getitem__(self, name):
            if name not in slot_tbl and (":" + name) not in slot_tbl:
                raise KeyError("unknown message argument: %s" % name)
            try:
                try:
                    relevant_slot = slot_tbl[name]
                except KeyError:
                    relevant_slot = slot_tbl[":" + name]
                return self.args[relevant_slot]
            except IndexError:
                return None
        def __setitem__(self, name, val):
            if name not in slot_tbl:
                raise KeyError("unknown message argument: %s" % name)
            pos = slot_tbl[name]
            _set_creating(self.args, pos, val)
        @classmethod
        def register(cls):
            """
            If the Message is subclassed to add custom behavior, this
            classmethod should be called on the subclass so that the
            IRCMessage.create() method knows to create the subclass
            rather than the superclass defined by MessageType(). Otherwise,
            IRCMessage.create() will default to the superclass

            The best practice is to use the @irc_message_representation
            decorator on the class as in this example.

            @irc_message_repreesntation
            class Privmsg(MessageType("privmsg", ["receivers", "message"])):
                pass # something interesting
            """
            message_representations[command]  = cls
        @classmethod
        def create(cls):
            """
            Creates a 'blank' instance of the message type by passing the
            necessary arguments to __init__.

            If you'd like to specify defaults for any of the arguments, then
            you should override this.
            """
            return cls(len(slots) * [None])
    Message.register()
    Message.__name__ == "Message<%s>" % command
    return Message


def irc_message_representation(c):
    """
    If you subclass a MessageType defined with the above, you should use this
    decorator to inform IRCMessage that the subclass is the true representation
    of the message type, rarther than the generated MessageType.

    See the example:

    @irc_message_representation
    class Privmsg(MessageType("privmsg", ["receivers", "message"])):
        pass # something interesting

    """
    c.register()
    return c
