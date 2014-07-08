"""
Paged output abstraction.
"""
from cmd_event import *
from rotational import Rotational
from System.Net import WebClient
from pastebin import pastebin
from StringIO import StringIO

paged_outputs = Rotational("pg")

PAGE_SIZE = 4

def segment(sequence, length):
    # Source: stackoverflow.com/questions/1218793/segment-a-list-in-python
    iterable = iter(sequence)
    def yield_length():
        for i in xrange(length):
            yield iterable.next()
    while True:
        res = list(yield_length())
        if not res:
            raise StopIteration
        yield res

@cmd_exporter
class IRCPagedOutputService(CMDService):
    @cmd_handler("page")
    def page(self, state, outputid, page):
        """
        PAGE pagedoutput page
        Displays the selected page of the paged output with the given ID.
        A paged output id looks like PG0001 or PG0040.
        """
        paged_outputs[outputid].present(state["irc"], int(page) - 1)
    @cmd_handler("paste")
    def paste(self, state, outputid):
        """
        PASTE pagedoutput
        Dumps the given paged output to a pastebin. Useful for long replies.
        A paged output id looks like PG0001 or PG0040.
        """
        url = pastebin("Paged output %s " % outputid.upper(),
            paged_outputs[outputid].dump())
        state["irc"].status("Pasted at: %s" % url)
    @cmd_handler("test_pagedoutput")
    def test_pagedoutput(self, state):
        """
        TEST_PAGEDOUTPUT
        Prints a roll of test paged output (400 ascending numbers).
        """
        state["irc"].add_lines(state, map(str, range(400)))
    def add(self, state, paged_output):
        name = paged_outputs.add(paged_output)
        paged_output.set_name(name)
        state["irc"].status(
            ("Beginning output for paged output %s. (HELP page or HELP" +
            " paste to view.)")
            % (name,))
        self.page(state, name, "1")
    def add_lines(self, state, lines):
        self.add(state, PagedOutput(lines))
    def patch(self, ircclient):
        ircclient.add_lines = self.add_lines
def _render(line):
    return line if isinstance(line, basestring) else line()
    # if line isn't a string, it's lazy so it's a callable


class PagedOutput(object):
    def __init__(self, lines):
        self.pages = list(segment(lines, PAGE_SIZE))
        self.name = None
    def set_name(self, name):
        self.name = name
    def present(self, ircclient, page_number):
        try:
            page = self.pages[page_number]
        except IndexError:
            ircclient.error("No such page.")
            return
        if page_number < 0:
            ircclient.error("Cannot access negative pages!")
            return
        ircclient.status("(%s) Page %s of %s."
            % (self.name, page_number + 1, len(self.pages)))
        for i in page:
            try:
                ircclient.status(_render(i))
            except Exception, e:
                irc.error("Error occurred while rendering this page: %s" % e)
    def dump(self):
        """
        Dumps all lines to text.
        """
        ou = []
        for i in self.pages:
            for l in i:
                ou.append(_render(l))
        return "\n".join(ou)
