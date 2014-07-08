from config import *
from System.Net import WebClient
from System.Collections.Specialized import NameValueCollection
from System.Text.Encoding import ASCII

import json
def pastebin(title, text):
    client = WebClient()
    client.Headers["User-Agent"] = PASTEBIN_AGENT
    params = NameValueCollection()
    params["data"] = text
    params["language"] = "text"
    params["name"] = PASTEBIN_AUTHOR
    params["title"] =  title
    params["private"] = PASTEBIN_PRIVATE
    params["expire"] = PASTEBIN_EXPIRE
    pg = client.UploadValues("http://pastebin.kde.org/api/json/create", "POST", params)
    g = ASCII.GetString(pg)
    print g
    result = json.loads(g)["result"]
    return "http://pastebin.kde.org/%s/%s" % (result["id"], result["hash"])
