from games.player import Player


class Action:   # Very generic action. It is just a data type.
    def __init__(self, player: Player):
        self.player = player

    def __str__(self):
        return "Action: Player " + (str(self.player.player_num) if self.player is not None else "")
