uuid_table = {}
def intern_uuid(uuid):
    try:
        return uuid_table[str(uuid)]
    except KeyError:
        uuid_table[str(uuid)] = uuid
        return uuid
