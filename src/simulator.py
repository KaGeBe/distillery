#!/usr/bin/env python3


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

    def __init__(self):
        self.field = [[[] for i in range(5)] for j in range(5)]
        self.last_move = None

    def place(self, x, y, color):
        place = self.field[x][y]
        if not len(place) == 0:
            raise GameLogicError("Not an empty field.")

        place.append(color)
        self.last_move = (x, y, color)

    def move(self, x0, y0, x1, y1, count):
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
        self.check_win(x1, y1)
        self.last_move = (x0, y0, x1, y1, count)

    def check_win(self, x, y):
        place = self.field[x][y]
        if len(place) > 4:
            print(str(place[-1]) + " has won.")

    def check_undo(self, x0, y0, x1, y1, count):
        if self.last_move == (x1, y1, x0, y0, count):
            raise MoveError(x0, y0, x1, y1, count, "Would undo the last move.")

    def check_sight(self, x0, y0, x1, y1, count):
        # TODO check nothing in between
        target_height = len(self.field[x1][y1])
        dist_x = abs(x1 - x0)
        dist_y = abs(y1 - y0)
        if dist_x == 0 and dist_y == 0:
            raise MoveError(x0, y0, x1, y1, count, "Origin == Target")
        elif dist_x == dist_y or dist_x == 0 or dist_y == 0:
            dist = max([dist_x, dist_y])
            if dist > target_height:
                raise MoveError(x0, y0, x1, y1, count,
                                "Distance {} too far from target tower of"
                                " height {}.".format(dist, target_height))
        else:
            raise MoveError(x0, y0, x1, y1, count, "Not in a valid direction.")

    def __str__(self):
        return "\n".join([" ".join([str(place) for place in row])
                         for row in self.field]) + "\n"


if __name__ == "__main__":
    sim = Simulator()
    print(sim)
    sim.place(0, 0, "R")
    print(sim)
    sim.place(2, 2, "R")
    print(sim)
    sim.place(2, 1, "R")
    print(sim)
    sim.move(2, 1, 2, 2, 1)
    print(sim)
    sim.place(3, 2, "W")
    print(sim)
    sim.move(2, 2, 3, 2, 1)
    print(sim)
    sim.place(3, 1, "R")
    for i in range(4):
        sim.place(3, 0, "R")
        sim.move(3, 0, 3, 1, 1)
