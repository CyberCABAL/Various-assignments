from . import Player


class ColourPlayer(Player):
    def __init__(self, player_num: int = 0, colour="b", name: str = "Player", initial_score: int = 0):
        super().__init__(player_num, name, initial_score)
        self.colour = colour

    def __str__(self):
        return "Player: " + str(self.player_num) + " (" + self.colour + ")\n" + "Name: " + self.name\
               + "\n" + "Score: " + str(self.score) + "\n"
