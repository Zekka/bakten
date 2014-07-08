import threading
from irc.service import Service
from rotational import Rotational

class DecisionService(Service):
    def __init__(self, ircclient):
        self.rotational = Rotational("dc")
        self.ircclient = ircclient
    def add(self, decision):
        name = self.rotational.add(decision)
        decision.set_name(name)
        decision.present(self.ircclient)
        return decision
    def _decide(self, decision_name, selection):
        decision_name = decision_name.upper()
        try:
            decision = self.rotational[decision_name]
            decision.fulfill(selection)
            del self.rotational[selection]
        except KeyError:
            raise DecisionError("no such decision: %s" % decision_name)
        except DecisionOptionError:
            raise DecisionError("not a valid option: %s" % selection)
    def decide(self, decision_name, selection):
        try:
            self._decide(decision_name, selection)
        except DecisionError, e:
            self.ircclient.error(e)
    def patch(self, ircclient):
        ircclient.add = self.add
        ircclient.decide = self.decide

class Decision(object):
    def __init__(self, text, choices):
        """
        Creates a decision, given its text as a string and a dict mapping
        {choice_name: callback}.
        """
        self.text = text
        self.choices = dict([(k.lower(), v) for k, v in choices.items()])
        self.name = "UNNAMED"
    def present(self, ircclient):
        """
        Prints an announcement message through the given IRCClient.
        """
        ircclient.status("Decision %s: %s (%s)" %
            (self.name, self.text, ", ".join(self.choices.keys()))
            )
    def fulfill(self, selection):
        """
        Attempts to fulfill the Decision by selecting a choice and running its
        callback.

        Raises a DecisionOptionError if the choice wasn't found.
        """
        try:
            callback = self.choices[selection.lower()]
        except KeyError:
            raise DecisionOptionError("no such choice: %s" % selection.lower())
        return callback()
    def set_name(self, name):
        """
        Sets the name of the Decision.
        """
        self.name = name

class DecisionOptionError(Exception): pass

class DecisionError(Exception): pass
