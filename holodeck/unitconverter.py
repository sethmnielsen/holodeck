import pint
import enum

from holodeck import HolodeckException


class UnitConverter:
    def __init__(self, source_units, target_units):
        self._source_units = source_units if source_units is not None else WorldUnitMapper()
        self._target_units = target_units if target_units is not None else WorldUnitMapper()

    @staticmethod
    def _convert_units(length, source, target):
        return length * target / source

    def to_target_length(self, length):
        return self.convert_units(length, self._source_units.get_length_units(), self._target_units.get_length_units())

    def to_source_length(self, length):
        return self.convert_units(length, self._target_units.get_length_units(), self._source_units.get_length_units())

    def to_target_weight(self, weight):
        return self.convert_units(weight, self._source_units.get_weight_units(), self._target_units.get_weight_units())

    def to_source_weight(self, weight):
        return self.convert_units(weight, self._target_units.get_weight_units(), self._source_units.get_weight_units())

    @staticmethod
    def _convert_coordinate(coordinate, source, target):
        if source.get_coordinate_frame == target.get_coordinate_frame:
            return  # do nothing
        if isinstance(coordinate, list) and len(coordinate) == 3:
            coordinate[1] *= -1
        else:
            raise HolodeckException("You must pass a list of 3 elements to successfully convert the coordinates")

    def set_source_units(self, source_units):
        self._source_units = source_units

    def set_target_units(self, target_units):
        self._target_units = target_units


class WorldUnitMapper:
    def __init__(self):
        register = pint.UnitRegistry()
        self.length = register.meter
        self.weight = register.kg
        self.coordinate_frame = CoordinateFrames.right_handed

    def set_weight(self, weight):
        self.weight = weight

    def set_length(self, length):
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
