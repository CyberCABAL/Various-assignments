from games.player import Player
from . import Action


class Place(Action):
    def __init__(self, point: tuple, player: Player = None):
        super().__init__(player)
        self.point = point

    def __str__(self):
        return super().__str__() + " places " + str(self.point)
