
from strategy import Strategy


class Simple_Strategy(Strategy):

    def __init__(self, color):
        self.color = color

    def next_action(self, simulator):
        for i in range(5):
            for j in range(5):
                if len(simulator.field[i][j]) == 0:
                    return (i, j)

        assert simulator.last_action != (0, 0, 0, 1, 1)
        return (0, 0, 0, 1, 1)

    def possible_moves():
        pass

    def rate_position(self, simulator):
        pass

    def __str__(self):
        return "Simple_Strategy({})".format(self.color)
