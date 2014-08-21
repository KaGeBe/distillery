#!/usr/bin/env python3


def compare(a, b):
    return (a > b) - (a < b)


class GameLogicError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MoveError(GameLogicError):

    def __init__(self, x0, y0, x1, y1, count=None, value=None):
        self.src = (x0, y0)
        self.tgt = (x1, y1)
        self.count = count
        self.value = value

    def __str__(self):
        return "Cannot move {} piece(s) from {} to {}: {}" \
               .format(self.count, self.src, self.tgt, self.value)


class Simulator:

    def __init__(self, first_player, second_player):
        self.field = [[[] for i in range(5)] for j in range(5)]
        self.last_action = None
        self.players = [first_player, second_player]

    def run(self, max_turns=None):
        turn = 0
        while max_turns is None or turn < max_turns:
            current_player = self.players[turn % 2]
            turn += 1
            action = current_player.next_action(self)
            print("Turn {} Player {}".format(turn, current_player))
            result = False
            if len(action) == 2:
                x, y = action
                result = self.place(x, y, current_player.color)
            else:
                x0, y0, x1, y1, count = action
                result = self.move(x0, y0, x1, y1, count)
            self.last_action = action
            print(self)
            if result:
                (win_color, x, y) = result
                print("Player {} has won on {}".format(win_color, (x, y)))
                return

    def place(self, x, y, color):
        print("Placing {} on {}.".format(color, (x, y)))
        place = self.field[x][y]
        if not len(place) == 0:
            raise GameLogicError("Not an empty field.")

        place.append(color)
        return False

    def move(self, x0, y0, x1, y1, count):
        print("Moving {} piece(s) from {} to {}."
              .format(count, (x0, y0), (x1, y1)))
        self.check_undo(x0, y0, x1, y1, count)

        place = self.field[x0][y0]
        if len(place) < count:
            raise MoveError(x0, y0, x1, y1, count,
                            "Not enough tower pieces at origin.")

        target_place = self.field[x1][y1]
        if len(target_place) == 0:
            raise MoveError(x0, y0, x1, y1, count,
                            "Target place does not have a tower.")

        self.check_sight(x0, y0, x1, y1, count)

        pieces = place[-count:]
        self.field[x1][y1].extend(pieces)
        del place[-count:]
        return self.check_win(x1, y1)

    def check_win(self, x, y):
        place = self.field[x][y]
        if len(place) > 4:
            return (place[-1], x, y)
        return False

    def check_undo(self, x0, y0, x1, y1, count):
        if self.last_action == (x1, y1, x0, y0, count):
            raise MoveError(x0, y0, x1, y1, count, "Would undo the last move.")

    def check_sight(self, x0, y0, x1, y1, count):
        target_height = len(self.field[x1][y1])
        dist_x = abs(x1 - x0)
        dist_y = abs(y1 - y0)
        dir_x = compare(x1, x0)
        dir_y = compare(y1, y0)
        if dist_x == 0 and dist_y == 0:
            raise MoveError(x0, y0, x1, y1, count, "Origin is equal target")
        elif dist_x == dist_y or dist_x == 0 or dist_y == 0:
            dist = max([dist_x, dist_y])
            if dist > target_height:
                raise MoveError(x0, y0, x1, y1, count,
                                "Distance {} too far from target tower of"
                                " height {}.".format(dist, target_height))
            # now checking that no tower between both fields
            for i in range(1, dist):
                x = x0 + (dir_x * i)
                y = y0 + (dir_y * i)
                place = self.field[x][y]
                if len(place) > 0:
                    raise MoveError(x0, y0, x1, y1, count,
                                    "Blocking tower in between at ({}, {})"
                                    .format(x, y))

        else:
            raise MoveError(x0, y0, x1, y1, count, "Not in a valid direction.")

    def __str__(self):
        return "\n".join([" ".join([str(place) for place in row])
                         for row in self.field]) + "\n"


if __name__ == "__main__":
    sim = Simulator()
    sim.place(3, 3, "R")
    sim.place(2, 2, "R")
    sim.move(3, 3, 2, 2, 1)
    sim.place(4, 4, "R")
    print(sim)
    sim.place(3, 3, "W")
    print(sim)
    sim.move(4, 4, 2, 2, 1)
    print(sim)
