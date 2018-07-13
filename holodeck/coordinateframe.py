import numpy as np

class CoordinateFrame:
    def __init__(self):
        self._coordinate = [1, 1, 1]

    def set_right_handed(self):
        self._coordinate = [1, -1, 1]

    def set_left_handed(self):
        self._coordinate = [1, 1, 1]

    def set_coordinate(self, coord):
        self._coordinate = coord

    def convert_coordinate(self, coord):
        for index, item in enumerate(coord):
            coord[index] = item * self._coordinate[index]



