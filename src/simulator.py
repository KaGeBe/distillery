#!/usr/bin/env python3


def compare(a, b):
    return (a > b) - (a < b)


class GameLogicError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MoveError(GameLogicError):

    def __init__(self, x0, y0, x1, y1, count=None, cause=None, cause_args=None):
        self.src = (x0, y0)
        self.tgt = (x1, y1)
        self.count = count
        self.cause = cause
        self.cause_args = cause_args

    def __str__(self):
        return "Cannot move {} piece(s) from {} to {}: " \
               .format(self.count, self.src, self.tgt) \
               + self.cause().format(**self.cause_args)


class MoveErrorCause:

    def origin_tower_too_small():
        return "Not enough tower pieces at origin."

    def no_target_tower():
        return "Target place does not have a tower."

    def invalid_direction():
        return "Invalid direction"

    def origin_equals_target():
        return "Origin is equal target"

    def distance_too_large():
        return "Distance {distance} too large to target of height {height}"

    def blocking_tower():
        return "Blocking tower in between at ({x}, {y})"

    def is_undo():
        return "Would undo the last move."


class Simulator:

    def __init__(self, first_player, second_player):
        self.field = [[[] for i in range(5)] for j in range(5)]
        self.last_action = None
        self.players = [first_player, second_player]
        self.colors = ['W', 'R']

    def run(self, max_turns=None):
        turn = 0
        while max_turns is None or turn < max_turns:
            current_player = self.players[turn % 2]
            current_color = self.colors[turn % 2]
            turn += 1
            action = current_player.next_action(self)
            print("Turn {} Player {}".format(turn, current_player))
            result = False
            if len(action) == 2:
                x, y = action
                result = self.place(x, y, current_color)
            elif len(action) == 5:
                x0, y0, x1, y1, count = action
                result = self.move(x0, y0, x1, y1, count)
            else:
                raise GameLogicError("Player action {} invalid".format(action))
            self.last_action = action
            print(self)
            if result:
                (win_color, x, y) = result
                print("Player {} has won on {}".format(win_color, (x, y)))
                return

    def get_tower(self, x, y):
        return self.field[x][y]

    def get_height(self, x, y):
        return len(self.get_tower(x, y))

    def place(self, x, y, color):
        print("Placing {} on {}.".format(color, (x, y)))
        place = self.field[x][y]
        if self.has_tower(x, y):
            raise GameLogicError("Not an empty field.")

        place.append(color)
        return False

    def has_tower(self, x, y):
        return self.get_height(x, y) > 0

    def move(self, x0, y0, x1, y1, count):
        print("Moving {} piece(s) from {} to {}."
              .format(count, (x0, y0), (x1, y1)))
        allowed, error_cause, cause_args = self.can_move(x0, y0, x1, y1, count)
        if not allowed:
            raise MoveError(x0, y0, x1, y1, count, error_cause, cause_args)

        place = self.field[x0][y0]
        pieces = place[-count:]
        self.field[x1][y1].extend(pieces)
        del place[-count:]
        return self.check_win(x1, y1)

    def check_win(self, x, y):
        place = self.field[x][y]
        if len(place) > 4:
            return (place[-1], x, y)
        return False

    def is_undo(self, x0, y0, x1, y1, count):
        return self.last_action == (x1, y1, x0, y0, count)

    def can_move(self, x0, y0, x1, y1, count):
        if self.is_undo(x0, y0, x1, y1, count):
            return (False, MoveErrorCause.is_undo, {})
        if len(self.field[x0][y0]) < count:
            return (False, MoveErrorCause.origin_tower_too_small, {})
        target_height = len(self.field[x1][y1])
        if target_height == 0:
            return (False, MoveErrorCause.no_target_tower, {})
        dist_x = abs(x1 - x0)
        dist_y = abs(y1 - y0)
        dir_x = compare(x1, x0)
        dir_y = compare(y1, y0)
        if dist_x == 0 and dist_y == 0:
            return (False, MoveErrorCause.origin_equals_target, {})
        elif dist_x == dist_y or dist_x == 0 or dist_y == 0:
            dist = max([dist_x, dist_y])
            if dist > target_height:
                return (False, MoveErrorCause.distance_too_large,
                        {"distance": dist, "height": target_height})
            # now check that no tower between both fields
            for i in range(1, dist):
                x = x0 + (dir_x * i)
                y = y0 + (dir_y * i)
                place = self.field[x][y]
                if len(place) > 0:
                    return (False, MoveErrorCause.blocking_tower,
                            {"x": x, "y": y})
            return (True, None, None)
        else:
            return (False, MoveErrorCause.invalid_direction)

    def __str__(self):
        return "\n".join([" ".join(["[{}]".format("".join(place))
                                   for place in row])
                         for row in self.field]) + "\n"


if __name__ == "__main__":
    sim = Simulator(None, None)
    sim.place(3, 3, "R")
    sim.place(2, 2, "R")
    sim.move(3, 3, 2, 2, 1)
    sim.place(4, 4, "R")
    print(sim)
    sim.place(3, 3, "W")
    print(sim)
    sim.move(4, 4, 2, 2, 1)
    print(sim)
