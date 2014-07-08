from transport import Transport, TransportError
from StringIO import StringIO
import time
import messages
import primitive
from services import IRCRules
import threading

class DelimitedReader(object):
    def __init__(self, delimiter = " "):
        self.progress = ""
        self.delimiter = delimiter
        self.callbacks = []
    def update(self, transport):
        if not transport.can_read():
            return
        content = transport.read()
        lines = []
        while True:
            line, delim, rest = content.partition(self.delimiter)
            if not delim:
                self.progress = line
                break
            lines.append(self.progress + line)
            self.progress = ""
            content = rest
        for l in lines:
            for c in self.callbacks:
                c(l)
    def add_callback(self, callback):
        self.callbacks.append(callback)

default_params = {
          "port"        : 6667
        , "user"        : "irc"
        , "realname"    : "IRC"
        }
class NOPARAM(object): pass
class IRCClient(object):
    COMMON_SERVICES = [IRCRules]
    def __init__(self, **params):
        self.params = params
        self.transport = Transport()
        self.reader = DelimitedReader("\r\n")
        self.reader.add_callback(self.new_line)
        self._services = []
        for t in type(self).COMMON_SERVICES:
            self.add_service(t())
        for i in self.services():
            self.add_service(i)
        self.lock_many = threading.Lock()
        self.lock_single = threading.Lock()

        self.common_state = {"irc": self}
            # This is not persistent and transmitted as the sender for
            # events like IRC commands

    def update_common_state(self, newstate):
        self.common_state.update(newstate)
    def get_common_state(self):
        return self.common_state
    def services(self):
        """
        Should return an Iterable of services initialized for the current
        instance.

        You should override this when subclassing IRCClient.
        """
        return []
    def loop(self):
        # Automates connect()/update() in a separate thread.
        self.looping = True
        self.state = load_state()
        threading.Thread(target = self._loop).start()
    def _loop(self):
        self.connect()
        while self.looping:
            time.sleep(0.01)
            self.update()
    def stop(self):
        dump_state(self.state)
        self.looping = False
    def connect(self):
        host, post = self.cfgget("host"), self.cfgget("port")
        self.transport.connect((host, post,))
        for i in self._services:
            i.handle(self, messages.JustConnected())
    def update(self):
        try:
            self.reader.update(self.transport)
        except TransportError:
            self.stop()
    def new_line(self, line):
        try:
            parsed = primitive.parse(line)
            print "Received line: %s" % line.strip()
        except primitive.UnknownMessageError:
            print "Received (but could not understand) line: %s" % line
            return
        for i in self._services:
            i.handle(self, parsed)
    def add_service(self, s):
        self._services.append(s)
        s.patch(self)
    def cfgget(self, name, default = NOPARAM):
        """
        Gets the given configuration parameter. The following order of
        precedence is used to return the parameter in order to deal with
        cases where it is unspecified:
            1. self.params[name]
            2. default
            3. default_params[name]
            4. None
        """
        try:
            return self.params[name]
        except KeyError:
            pass
        if default != NOPARAM: return default
        try:
            return default_params[name]
        except KeyError:
            pass
        return None
    def cfgset(self, name, value):
        self.params[name] = value
    def send(self, message):
        """
        Sends a single message.

        This method is thread-safe: however, it's probably best to use sendmany
        if you're attempting to send a series of messages at once, so that
        unrelated send-multiple-messages requests don't intersect
        accidentally.
        """
        with self.lock_single:
            out = message.write()
            print "Sending line: %s" % out
            self.transport.write(out + "\r\n")
    def sendmany(self, messages):
        """
        Sends several messages at once.

        Because the bot is heavily threaded and threads are evil, it's probably
        best to call sendmany() instead of calling send multiple times when
        sending series of messages, so unrelated series don't occur at the same
        time.

        There's no danger of two messages sending inside of each other
        midstream, mind, as Transport.write() and self.send() are both highly
        thread-safe.
        """
        with self.lock_many:
            for i in messages:
                self.send(i)
    def quit(self, message = None):
        q = messages.QuitMessage.create()
        q["text"] = message
        self.send(q)
        self.stop()
    """
    Most IRC messages are not wrapped in order to
    encourage users to use threadsafe ones like sendmany.
    """
    def status(self, text):
        """
        You should override this in an IRC subclass as a default 'send some
        message' routine.
        """
        pass
    def error(self, text):
        """
        A special version of status() to be used with errors.

        By default this just prepends ERROR: to the message and calls status().

        You can override this.
        """
        self.status("ERROR: %s" % text)

import pickle
    # Although most state will probably be representable in JSON, other
    # programmers are lazy so we should probably let them use pickle

STATE_LOCATION = "state"
def load_state():
    try:
        with open(STATE_LOCATION, "rt") as f:
            return pickle.load(f)
    except IOError: # the file didn't exist
        return {}
def dump_state(state):
    with open(STATE_LOCATION, "wt") as f:
        pickle.dump(state, f)

if __name__ == "__main__":
    g = IRCClient(host = "irc.boredicons.com", nick = "Bakten")
    g.loop()
