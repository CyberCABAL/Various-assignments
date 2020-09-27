from games.player import Player
from . import Action


class Remove(Action):
    def __init__(self, amount: int, player: Player = None):
        super().__init__(player)
        self.amount = amount

    def __str__(self):
        return super().__str__() + " removes " + str(self.amount)
