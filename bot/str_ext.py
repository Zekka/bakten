def splitlines(s, width):
    return "\n".join(map(lambda x: _splitlines(x, width), s.split("\n")))
def _splitlines(s, width):
    remaining = s
    out = []
    while len(remaining) > 0:
        out.append(remaining[:width])
        remaining = remaining[width:]
    return "\n".join(out)
