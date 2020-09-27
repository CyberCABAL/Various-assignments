# A game piece of any sort. Maybe colour shouldn't be here?
class GameUnit:
    def __init__(self, colour="black", owner_num: int = -1, location: tuple = (0, 0)):
        self.owner_num = owner_num
        self.colour = colour
        self.location = location

    def __str__(self):
        owner = "Game unit at " + str(self.location) + "."
        if self.owner_num > 0:
            owner = " Owned by player " + str(self.owner_num) + "."
        return owner + " Colour: " + self.colour + ".\n"
