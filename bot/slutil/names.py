from System.Collections.Generic import List
from OpenMetaverse import UUID
from ..rotational import Rotational

people = Rotational("av")

class AvatarNames(object):
    name_table = {} # this can be global, it can't differ between instances
    reverse_name_table = {}
    @classmethod
    def add_name(cls, success, names, badIDs):
        if success:
            for i in names:
                cls.name_table[i.ID] = i.DisplayName
                cls.reverse_name_table[i.DisplayName.lower()] = i.ID
    @classmethod
    def name_from_uuid(cls, state, uuid):
        if uuid in cls.name_table:
            return cls.name_table[uuid]
        else:
            l = List[UUID]()
            l.Add(uuid)
            state["sl"].Avatars.GetDisplayNames(l, cls.add_name)
            return None
    @classmethod
    def uuid_from_name(cls, state, name):
        if name.lower() in cls.reverse_name_table:
            return cls.reverse_name_table[name.lower()]
        else: # shouldn't happen unless the name given was a typo
            return None

def name_of(state, avatar):
    return "[{0}] [{1} ({2}]".format(*[
        people.add(avatar.ID),
        AvatarNames.name_from_uuid(state, avatar.ID) if
            AvatarNames.name_from_uuid(state, avatar.ID)
            else "[display name pending]",
        avatar.Name])
        
