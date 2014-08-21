
from strategy import Strategy


class Trivial_Strategy(Strategy):

    def __init__(self, color):
        Strategy.__init__(self, color)

    def next_action(self, simulator):
        for i in range(5):
            for j in range(5):
                if len(simulator.field[i][j]) == 0:
                    return (i, j)

        assert simulator.last_action != (0, 0, 0, 1, 1)
        return (0, 0, 0, 1, 1)

    def __str__(self):
        return "Trivial_Strategy({})".format(self.color)
