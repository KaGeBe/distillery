#!/usr/bin/env python3

from trivial_strategy import Trivial_Strategy
from all_actions_strategy import AllActionsStrategy
from player import CommandLinePlayer
from simulator import Simulator

if __name__ == "__main__":
    # white = Trivial_Strategy("W")
    # red = Trivial_Strategy("R")
    white = AllActionsStrategy("W")
    # red = AllActionsStrategy("R")
    red = CommandLinePlayer("R")
    sim = Simulator(white, red)
    sim.run()
