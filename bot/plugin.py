import os.path
from util import memoize
import sys
import imp

@memoize
def find_plugins(directory):
    return list(_find_plugins(directory))

def _find_plugins(directory):
    for module in os.listdir(directory):
        if module == '__init__.py' or (not module.endswith(".py")): continue
        yield imp.load_source("bot.%s" % module[:-3], os.path.join(directory, module))
