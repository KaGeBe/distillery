
class Strategy(AbstractStrategy):

    def __init__(self,color):
        self.color = color

    def next_move(simulator):
        for i in range(5):
            for j in range(5):
                if field[i][j] == []:
                    simulator.place(x,y,self.color)
                    return simulator
        
        simulator.move(0,0,0,1,1)
        return simulator
        
        