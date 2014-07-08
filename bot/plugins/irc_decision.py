"""
Managing decisions.
"""
from cmd_event import cmd_handler, cmd_exporter, CMDService
from config import *
from decision import Decision

@cmd_exporter
class IRCDecisionSystem(CMDService):
    @cmd_handler("decide")
    def decide(self, state, decision_name, selection):
        """
        DECIDE decision_name selection
        Responds to a decision.
        """
        state["irc"].decide(decision_name, selection)
    @cmd_handler("test_decision")
    def test_decision(self, state):
        """
        TEST_DECISION
        Creates a test decision.
        """
        def yes():
            state["irc"].status(
                "Here it is! (it wasn't all that surprising, was it?)")
        def no():
            state["irc"].status(
                "Too bad! (this was it)")
        testdecision = Decision("Do you want a special surprise?",
            {
                "yes": yes,
                "no" : no
            })
        state["irc"].add(testdecision)
