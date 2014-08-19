#!/usr/bin/env python3


class Simulator:

    def __init__(self):
        self.field = [[[] for i in range(5)] for j in range(5)]
        self.last_move = None

    def place(self, x, y, color):
        place = self.field[y][x]
        assert len(place) == 0
        place.append(color)

    def move(self, source_x, source_y, target_x, target_y, count):
        place = self.field[source_y][source_x]
        assert len(place) >= count
        stack = place[-count:]
        target_place = self.field[target_y][target_x]
        assert len(target_place) > 0
        # TODO distance check
        self.field[target_y][target_x].extend(stack)
        del place[-count:]
        self.check_win(target_x, target_y)

    def check_win(self, x, y):
        place = self.field[y][x]
        if len(place) > 4:
            print(str(place[-1]) + " has won.")

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
