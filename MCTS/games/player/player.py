
class Player:
    def __init__(self, player_num: int = 0, name: str = "Player", initial_score: int = 0):
        self.player_num = player_num
        self.name = name
        self.score = initial_score

    def __str__(self):
        return "Player: " + str(self.player_num) + "\n" + "Name: " + self.name + "\n" + "Score: " + str(self.score) + "\n"
