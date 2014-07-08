"""
Deals with ourself.
"""
from sl_event import sl_handler, sl_exporter, SLService
import OpenMetaverse

@sl_exporter
class AgentHandler(SLService):
    @sl_handler("AlertMessage")
    def on_alert(self, state, sender, args):
        state["irc"].status("Alert: %s" % args.Message);
