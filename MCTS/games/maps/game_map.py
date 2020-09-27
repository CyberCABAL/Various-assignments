import abc


# Generic game map.
class GameMap:
    __metaclass__ = abc.ABCMeta

    def __init__(self, map_data):
        self.map_data = map_data

    @abc.abstractmethod
    def get_distance(self, from_point, to_point) -> int:
        pass

    @abc.abstractmethod
    def get_neighbour_points(self, location) -> list:
        pass

    @abc.abstractmethod
    def is_neighbour(self, location_0, location_1) -> bool:
        pass

    @abc.abstractmethod
    def get(self, location):
        pass

    @abc.abstractmethod
    def set(self, location, value):
        pass

    def set_map(self, map_data, *args):
        self.map_data = map_data

    def get_map(self):
        return self.map_data

    @abc.abstractmethod
    def get_data(self):
        return self.map_data

    @abc.abstractmethod
    def __distance_estimate(self, from_location, to_location) -> int:
        pass
