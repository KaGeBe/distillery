from simulator import GameLogicError


class CommandLinePlayer:

    def __init__(self, color):
        self.color = color

    def next_action(self, simulator):
        print("Input next action. Either 'M x0 y0 x1 y1 c' or 'P x y'.")
        player_action = None
        while not player_action:
            try:
                player_action = input()
                split = player_action.split()
                if not len(split) in [3, 6]:
                    raise GameLogicError("Invalid action format.")
                if split[0] == "M":
                    if not len(split) == 6:
                        raise GameLogicError("Invalid move action format.")
                    return tuple([int(s) for s in split[1:]])
                if split[0] == "P":
                    if not len(split) == 3:
                        raise GameLogicError("Invalid place action format.")
                    return tuple([int(s) for s in split[1:]])
            except Exception as e:
                print("Invalid action ({}), try again.".format(e))
                player_action = None

    def __str__(self):
        return "CommandLinePlayer({})".format(self.color)
