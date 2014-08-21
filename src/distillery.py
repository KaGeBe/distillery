#!/usr/bin/env python3

from trivial_strategy import Trivial_Strategy
from simulator import Simulator

if __name__ == "__main__":
    trivial_white = Trivial_Strategy("W")
    trivial_red = Trivial_Strategy("R")
    sim = Simulator(trivial_white, trivial_red)
    sim.run()
