import enum
from .exceptions import HolodeckException
from pint import UnitRegistry


class UnitConverter:
    def __init__(self, native_units, foreign_units):
        self._native_units = native_units if native_units is not None else WorldUnits()
        self._foreign_units = foreign_units if foreign_units is not None else WorldUnits()

    @staticmethod
    def _convert_units(length, source, target):
        return length * target / source

    def to_foreign_length(self, length):
        return self._convert_units(length, self._native_units.get_length_units(), self._foreign_units.get_length_units())

    def to_native_length(self, length):
        return self._convert_units(length, self._foreign_units.get_length_units(), self._native_units.get_length_units())

    def to_foreign_weight(self, weight):
        return self._convert_units(weight, self._native_units.get_weight_units(), self._foreign_units.get_weight_units())

    def to_native_weight(self, weight):
        return self._convert_units(weight, self._foreign_units.get_weight_units(), self._native_units.get_weight_units())

    def to_native_coordinate_frame(self, coordinate):
        return self._convert_coordinate(coordinate, self._foreign_units, self._native_units)

    def to_foreign_coordinate_frame(self, coordinate):
        return self._convert_coordinate(coordinate, self._native_units, self._foreign_units)

    @staticmethod
    def _convert_coordinate(coordinate, source, target):
        if source.get_coordinate_frame == target.get_coordinate_frame:
            return  # do nothing
        if isinstance(coordinate, list) and len(coordinate) == 3:
            coordinate[1] *= -1
        else:
            raise HolodeckException("You must pass a list of 3 elements to successfully convert the coordinates")

    def set_native_units(self, native_units):
        self._native_units = native_units

    def set_foreign_units(self, foreign_units):
        self._foreign_units = foreign_units


class WorldUnits:
    def __init__(self):
        self.register = UnitRegistry()
        self.length = self.register.cm
        self.weight = self.register.kg
        self.coordinate_frame = CoordinateFrames.right_handed

    def set_weight(self, weight):
        if isinstance(weight, str):
            self.weight = getattr(self.register, weight)()
        else:
            self.weight = weight

    def set_length(self, length):
        if isinstance(length, str):
            self.weight = getattr(self.register, length)()
        else:
            self.length = length

    def set_coordinate_frame(self, coordinate_frame):
        self.coordinate_frame = coordinate_frame

    def get_length_units(self):
        return self.length

    def get_weight_units(self):
        return self.weight

    def get_coordinate_frame(self):
        return self.coordinate_frame


class CoordinateFrames(enum.Enum):
    left_handed = 1
    right_handed = 2


class UnitType(enum.Enum):
    length = 1
    weight = 2
    force = 3
    time = 4
