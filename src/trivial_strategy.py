
from strategy import *
import simulator

class Trivial_Strategy(Strategy):

    def __init__(self,color):
        self.color = color

    def next_move(self,simulator):
        for i in range(5):
            for j in range(5):
                if simulator.field[i][j] == []:
                    simulator.place(i,j,self.color)
                    return
        
        assert simulator.last_move != (0,0,0,1,1)
        simulator.move(0,0,0,1,1)
        return
        