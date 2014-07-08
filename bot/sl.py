from OpenMetaverse import GridClient, SimConnectingEventArgs, SimConnectedEventArgs
from System import EventHandler, EventArgs
from config import *
from plugin import find_plugins
import events

def make_params(cli, user_fname     = USER_FNAME
                   , user_lname     = USER_LNAME
                   , password       = PASSWORD
                   , client         = CLIENT
                   , version        = VERSION):
    return cli.Network.DefaultLoginParams(user_fname, user_lname, password, client, version)

class Session(object):
    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        self.cli = GridClient(*args, **kwargs)
        self.params = make_params(self.cli, *args, **kwargs)
        for name, val in SETTINGS.items():
            setattr(self.cli.Settings, name, val)
        self.controller.update_common_state({"sl": self.cli})
    def start(self):
        def build_events(x):
            cli_responder_net = events.responder_for(x)
            cli_responder_net.set_common_state(
                self.controller.get_common_state() 
                )
            create_handlers(cli_responder_net)

        map(build_events, self.eventy_things)
        self.cli.Network.Login(self.params)

    def stop(self):
        self.cli.Network.Logout()

    @property
    def eventy_things(self):
        yield self.cli.Assets
        yield self.cli.Avatars
        yield self.cli.Directory
        yield self.cli.Estate
        yield self.cli.Friends
        yield self.cli.Grid
        yield self.cli.Groups
        yield self.cli.Inventory
        yield self.cli.Network
        yield self.cli.Objects
        yield self.cli.Parcels
        yield self.cli.Self
        yield self.cli.Sound
        yield self.cli.Terrain

def create_handlers(responder):
    for i in find_plugins(PLUGIN_DIR):
        responder.add_module(i)
