import socket
import select
from StringIO import StringIO
import threading
import time
class CuttingStringIO(object):
    def __init__(self):
        self.io = StringIO()
        self.lock = threading.Lock()
    def write(self, tx):
        with self.lock:
            self.io.write(tx)
    def read(self, amount = None):
        with self.lock:
            io_cnt = self.io.getvalue()
            out = io_cnt[:amount] if amount != None else io_cnt
            rest = io_cnt[amount:] if amount != None else ""
            self.io = StringIO(rest) # drop old text
            return out
    def __len__(self):
        # Returns how much data is left in the CuttingStringIO
        return len(self.io.getvalue())
    # no getvalue method because anything read is dropped

class Transport(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting = CuttingStringIO()
        self.lock = threading.Lock()
        self.connected = False
    def connect(self, target):
        # target: (host, port)
        self.socket.connect(target)
        # self.socket.setblocking(False)
        self.connected = True
    def read(self, amount = None):
       if not self.connected:
            raise TransportError("transport not connected")
       with self.lock:
            while (len(self.waiting) < amount if amount else self.can_read()):
                g = self.socket.recv(8192)
                if len(g) == 0:
                    raise TransportError("connection broken during recv")
                    # TODO: should I raise a TranportError?
                self.waiting.write(g)
                time.sleep(.01)
            return self.waiting.read(amount)
    def write(self, txt):
        if not self.connected:
            raise TransportError("transport not connected")
        with self.lock:
            try:
               self.socket.sendall(txt)
            except socket.error, e:
                raise TransportError("socket send failed: %s" % e.message)
    def disconnect(self):
        self.socket.shutdown()
        self.socket.close()
        self.connected = False
    def can_read(self):
        r, _, _ = select.select([self.socket], [], [], 0)
        return len(r) > 0
    def can_write(self):
        _, w, _ = select.select([], [self.socket], [], 0)
        return len(w) > 0

class TransportError(Exception): pass
