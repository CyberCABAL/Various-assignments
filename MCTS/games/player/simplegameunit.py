from . import GameUnit


# It is simple by the fact that it prints only as its colour.
class SimpleGameUnit(GameUnit):
    def __init__(self, colour="b", owner_num: int = -1, location: tuple = (0, 0)):
        super().__init__(colour, owner_num, location)

    def __str__(self):
        return self.colour
