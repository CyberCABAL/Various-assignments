class HexagonGrid:  # Simple data structure for triangle and square hex grids.
    def __init__(self, array2d, triangle=None):
        self.data = array2d
        self.len_y = len(array2d)
        self.triangle = triangle if triangle is not None else self.len_y == len(self.data[int(self.len_y / 2)])

    def get(self, point: tuple):
        return self.data[point[1]][point[0]]

    def set(self, point: tuple, value):
        self.data[point[1]][point[0]] = value

    def set_data(self, array2d: list):
        self.data = array2d

    def get_data(self) -> list:
        return self.data
