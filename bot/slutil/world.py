from OpenMetaverse import UUID, Vector3, Avatar
from System import Action, Predicate
from System.Collections.Generic import KeyValuePair
from ..rotational import Rotational
def where_in_the_hell_is(client, avatar_uuid):
    # Ported from http://lib.openmetaverse.org/wiki/WhereInTheHellis
    """
    def is_right_one(avy):
        out = str(avy.ID) == str(avatar_uuid)
        print "Current: %s" % avy.ID
        print "Target: %s" % avatar_uuid
        return out
    answer = Vector3.Zero
    avatar = client.Network.CurrentSim.ObjectsAvatars.Find(
            Predicate[Avatar](is_right_one)
            )
    print avatar
    if avatar != None:
        if avatar.ParentID == 0: # not sitting
            answer = avatar.Position
        else:
            p = client.Network.CurrentSim.ObjectsPrimitives.Find(
                lambda p: p.LocalID == avatar.ParentID
                )
            if p != None:
                answer = p.Position
    return answer
    """
    d = client.Network.CurrentSim.AvatarPositions
    return d[avatar_uuid] if d.ContainsKey(avatar_uuid) else None

places = Rotational("pl")
