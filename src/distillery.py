#!/usr/bin/env python3

import strategy
from trivialStrategy import *
from simple_strategy import *
from simulator import *

if __name__ == "__main__":
    print ("Purifying liquids...")
    sim = Simulator()
    trivial_white = Trivial_Strategy("white")
    trivial_red = Simple_Strategy("red")
    turn = "white"
    turn_no = 1
    while (turn_no<1000):
        print ("Turn ", turn_no, ": Player ", turn, " is moving")
        if turn == "white":
            trivial_white.next_move(sim)
        else:
            trivial_red.next_move(sim)
        
        turn_no += 1