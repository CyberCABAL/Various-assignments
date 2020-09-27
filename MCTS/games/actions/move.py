from games.player import Player
from . import Action


class Move(Action):
    def __init__(self, from_point: tuple, to_point: tuple, player: Player = None):
        super().__init__(player)
        self.from_point = from_point
        self.to_point = to_point

    def __str__(self):
        return (super().__str__() + " moves " if self.player is not None else "Action: Moves ")\
               + str(self.from_point) + " to " + str(self.to_point) + "."
