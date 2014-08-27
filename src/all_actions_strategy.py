from strategy import Strategy
import random


class AllActionsStrategy(Strategy):

    def __init__(self, color):
        self.color = color

    def add_moves(self, simulator, x, y, possible_moves):
        source_height = simulator.get_height(x, y)
        for dir_x in [-1, 0, 1]:
            for dir_y in [-1, 0, 1]:
                if dir_x == dir_y == 0:
                    continue
                # find next tower
                target_x = x + dir_x
                target_y = y + dir_y
                distance = 1
                while -1 < target_x < 5 and -1 < target_y < 5:
                    height = simulator.get_height(target_x, target_y)
                    if height >= distance:
                        for count in range(1, source_height + 1):
                            possible_moves.add(
                                (x, y, target_x, target_y, count))
                    if height > 0:
                        break
                    target_x += dir_x
                    target_y += dir_y
                    distance += 1

    def all_actions(self, simulator):
        places = set()
        moves = set()
        for x in range(5):
            for y in range(5):
                if not simulator.has_tower(x, y):
                    places.add((x, y))
                else:
                    self.add_moves(simulator, x, y, moves)
        print(places)
        print(moves)
        return (places, moves)

    def next_action(self, simulator):
        places, moves = self.all_actions(simulator)

        return random.sample(moves.union(places), 1)[0]

    def action_score(self, simulator, action):
        pass

    def __str__(self):
        return "AllActionsStrategy({})".format(self.color)
