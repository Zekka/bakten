from sl_event import *
from cmd_event import *
from OpenMetaverse import *
from slutil.names import AvatarNames
import traceback
from collections import deque
from slutil.world import places
from str_ext import splitlines

@sl_exporter
class DirectoryService(SLService):
    def handle_list(self, parcs, query):
        parcels = list(parcs)
        Search.callbacks.popleft()(parcels)
    @sl_handler("PlacesReply")
    def handle_places_reply(self, state, sender, args):
        self.handle_list(args.MatchedPlaces, args.QueryID)

class Search(object):
    callbacks = deque()
        # Originally used a dict mapping query ids to their result callbacks,
        # but that turned out to be unreliable.
    def __init__(self, keywords, search_func, present_func):
        self.search_func = search_func
        self.present_func = present_func
        self.keywords = keywords
    def present(self, state):
        def update_and_present(entries):
            state["irc"].add_lines(state, [
                (lambda x: lambda: self.present_func(x))(e) # lazy output
                for e in entries])

        self.search_func(self.keywords)
        type(self).callbacks.append(update_and_present)

PAGE_SIZE = 4
@cmd_exporter
class DirectoryCommands(CMDService):
    @takes_full_message
    @cmd_handler("places")
    def places(self, state, keywords):
        """
        PLACES searchterms
        Searches the SL Directory for places matching the given search terms
        """
        active_search = Search(keywords,
            state["sl"].Directory.StartPlacesSearch,           
            lambda i: "[%s]: %s (traffic: %s)" % (places.add(i), i.Name, i.Dwell,))
        active_search.present(state)
    @cmd_handler("meta")
    def meta(self, state, placeid):
        """
        META placeid
        Prints a detailed description of a place's metadata, given its id.
        A place id looks like PL0040 or PL0069.
        """
        place = places[placeid]
        state["irc"].add_lines(state, """
        {name} ([{id}])
        {desc}
        (visitor URL: {url})
        """.format(**{
                "name"  : place.Name,
                "id"    : placeid.upper(),
                "desc"  : splitlines(place.Desc.strip(), 200),
                "url"   : place.ToSLurl(),
            }).strip().split("\n")
        )
