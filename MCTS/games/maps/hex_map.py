from games.maps import GameMap
from data_types import HexagonGrid


# Hexagonal map.
class HexMap(GameMap):

    def __init__(self, map_data: HexagonGrid, tabs: int = 1):
        super().__init__(map_data)

        self.tab = "\t" * tabs
        self.__double_tab = self.tab * 2

    def get_distance(self, from_point, to_point) -> int:
        current = from_point
        distance = 0

        while current != to_point:  # A simple greedy search that goes by a heuristic of approximated distance. Optimal.
            neighbours = self.get_neighbour_points(current)
            if not neighbours:
                return -1

            best = self.__distance_estimate(current, to_point)
            best_n = current
            for n in neighbours:
                estimate = self.__distance_estimate(n, to_point)
                if estimate < best:
                    best_n = n
                    best = estimate

            current = best_n
            distance += 1
        return distance

    def get_neighbour_points(self, point: tuple) -> list:
        neighbours = []

        map_now = self.get_data()

        x, y = point
        if x > 0:
            neighbours.append((x - 1, y))
            if y < self.map_data.len_y - 1:
                neighbours.append((x - 1, y + 1))

        if y < self.map_data.len_y - 1 and x < len(map_now[y + 1]):
            neighbours.append((x, y + 1))

        if x < len(map_now[y]) - 1:
            neighbours.append((x + 1, y))

        if y > 0:
            neighbours.append((x, y - 1))

            if (self.map_data.triangle and x < len(map_now[y - 1])) or x < len(map_now[y - 1]) - 1:
                neighbours.append((x + 1, y - 1))

        return neighbours

    def is_neighbour(self, point_0: tuple, point_1: tuple) -> bool:
        x_delta = abs(point_0[0] - point_1[0])
        y_delta = abs(point_0[1] - point_1[1])

        if x_delta > 1 or y_delta > 1 or point_0[0] == point_1[0] and point_0[1] == point_1[1]:
            return False
        if (point_0[0] == point_1[0]) != (point_0[1] == point_1[1]):
            return True
        if point_0[0] < point_1[0] and point_0[1] < point_1[1] or point_1[0] < point_0[0] and point_1[1] < point_0[1]:
            return True

    def get(self, point: tuple):
        return self.map_data.get(point)

    def set(self, point: tuple, value):
        self.map_data.set(point, value)

    def set_map(self, map_data: HexagonGrid, *args):
        self.map_data = map_data

    def get_map(self) -> HexagonGrid:
        return self.map_data

    def get_data(self):
        return self.map_data.get_data()

    def get_center(self, f: tuple, t: tuple) -> tuple:     # Works best when the number is even, map dependent.
        return int((t[0] + f[0]) / 2), int((t[1] + f[1]) / 2)

    def __distance_estimate(self, from_p: tuple, to_p: tuple) -> int:   # For a simple greedy search process.
        return abs(from_p[0] - to_p[0]) + abs(from_p[1] - to_p[1])

    def display_format(self, triangle=None) -> str:
        map_now = self.get_data()

        tri = self.map_data.triangle if triangle is None else triangle
        string = ""
        for y in range(self.map_data.len_y):
            indent = ""
            n = y

            for tab in range(int((self.map_data.len_y - y) + 0.5) - 1):
                indent += self.tab
            string += indent
            substring = "\n" + indent
            for x in range(y + 1):
                string += " " + str(map_now[n][x])
                if x < y:
                    string += self.tab + " -" + self.tab
                n -= 1

                if not tri:
                    if y < self.map_data.len_y - 1 or 0 < x < y:
                        substring += "/ \\" + self.__double_tab
                    elif 0 < x:
                        substring += "/"
                    else:
                        substring += "  \\" + self.__double_tab
                elif y < self.map_data.len_y - 1:
                    substring += "/ \\" + self.__double_tab

            string += substring + "\n"

        if not tri:
            for x in range(0, len(map_now[-1]) - 1):
                indent = ""
                for tab in range(int(x + 0.5) + 1):
                    indent += self.tab
                string += indent
                substring = "\n" + indent

                if x < len(map_now[-1]) - 2:
                    substring += "  \\" + self.__double_tab

                temp_xlen = len(map_now[-x]) - x
                for y in range(1, temp_xlen):
                    string += " " + str(map_now[-y][y + x])

                    if y < temp_xlen - 1:
                        string += self.tab + " -" + self.tab
                        if y < temp_xlen - 2:
                            substring += "/ \\" + self.__double_tab
                        else:
                            substring += "/"
                string += substring + "\n"
        return string

    def __str__(self):
        string = ""
        map_now = self.get_data()

        for y in range(self.map_data.len_y):
            substring = "\n"
            for x in range(len(map_now[y])):
                string += str(map_now[y][x])

                if x < len(map_now[y]) - 1:
                    string += self.tab + "-" + self.tab
                    if y < self.map_data.len_y - 1:
                        substring += "|" + self.tab + "/ " + self.tab
                else:
                    if y < self.map_data.len_y - 1 and not (self.map_data.triangle or x < len(map_now[y]) - 2):
                        substring += "|"
            string += substring + "\n"
        return string
