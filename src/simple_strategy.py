
from strategy import *
import simulator

class Simple_Strategy(Strategy):

    def __init__(self,color):
        self.color = color

    def next_move(self,simulator):
        for i in range(5):
            for j in range(5):
                if len(simulator.field[i][j]) == 0:
                    simulator.place(j,i,self.color)
                    return
        
        assert simulator.last_move != (0,0,0,1,1)
        simulator.move(0,0,0,1,1)
        return
        
    def possible_moves():
        pass
        
    def rate_position(self,simulator):
        pass