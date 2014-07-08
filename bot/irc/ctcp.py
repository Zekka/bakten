mquote = "\x10"
def quote(msg):
    return (msg.replace(mquote, mquote + mquote)
                .replace("\x00", mquote + "0")
                .replace("\n", mquote + "n")
                .replace("\r", mquote + "r")
                )

def unquote(msg):
    return (msg.replace(mquote + r, "\r")
                .replace(mquote + n, "\n")
                .replace(mquote + 0, "\x00")
                .replace(mquote + mquote, mquote)
                .replace(mquote, "")
                )
xdelim = "\x01"
