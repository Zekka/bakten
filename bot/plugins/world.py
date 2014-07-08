from sl_event import *
from cmd_event import *
from slutil.names import AvatarNames, people, name_of
from slutil.world import where_in_the_hell_is, places
from OpenMetaverse import Vector3, Avatar
from System import Action
@sl_exporter
class WorldEvents(SLService):
    pass

@cmd_exporter
class WorldCommands(CMDService):
    @takes_full_message
    @cmd_handler("approach")
    def approach(self, state, player):
        """
        APPROACH player
        Attempts to move to the position of the given nearby player. Specify the player by their display name (i.e. Shaiming Hao, Bakten)
        """
        uuid = people.get(player)
        if uuid == None:
            state["irc"].error("Was not able to find a target of that name.")
            return
        g = where_in_the_hell_is(state["sl"], uuid)
        if g == Vector3.Zero:
            state["irc"].error("Found target, but it was not in the current sim.")
            return
        state["sl"].Self.AutoPilotLocal(g.X, g.Y, g.Z)
        state["irc"].status("Approaching target.")
    @cmd_handler("stop")
    def stop(self, state):
        """
        STOP
        If we are currently APPROACHing, stop us.
        """
        state["sl"].Self.AutoPilotCancel()
    @cmd_handler("tele")
    def tele(self, state, location):
        """
        TELE placeid
        Teleports to a given place.
        A placeid looks like PL0010 or PL0455
        """
        if location not in places:
            state["irc"].error("That's not a place I recognize.")
            return
        parc = places[location]
        sim = parc.SimName
        x, y, z = map(float, parc.ToSLurl().split("/")[-3:])
        # this seems to be actually the most reasonable way to
        # get local x, y, and z
        success = state["sl"].Self.Teleport(sim, Vector3(x, y, z))
        
        if success:
            state["irc"].status("Entering time warp...")
        else:
            state["irc"].status("For some unknown reason I've failed to teleport.")
    @cmd_handler("scan")
    def scan(self, state):
        """
        SCAN
        Scans the region for people.
        """

        sim = state["sl"].Network.CurrentSim
        avs = []
        def add_av(avatar):
            avs.append(avatar)
        sim.ObjectsAvatars.ForEach(Action[Avatar](add_av))

        distance_to_self = lambda av: Vector3.Distance(av.Position,
                state["sl"].Self.SimPosition)

        avs.sort(key = distance_to_self)

        lines = ["Avatars found:"]
        for i in avs:
            lines.append("%s (distance %s)" % (
                name_of(state, i),
                distance_to_self(i)
                ,))

        state["irc"].add_lines(state, lines)
