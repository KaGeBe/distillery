#!/usr/bin/env python3

from trivial_strategy import *
from simple_strategy import *
from simulator import *

if __name__ == "__main__":
    sim = Simulator()
    trivial_white = Trivial_Strategy("W")
    trivial_red = Trivial_Strategy("R")
    turn = "white"
    turn_no = 1
    won = False
    print(sim)
    while not won and turn_no < 1000:
        print("Turn ", turn_no, ": Player ", turn, " is moving")
        if turn == "white":
            won = trivial_white.next_move(sim)
            turn = "red"
        else:
            won = trivial_red.next_move(sim)
            turn = "white"
        turn_no += 1
        print(sim)
    if won:
        (win_color, x, y) = won
        print("Player {} has won on {}".format(win_color, (x, y)))
