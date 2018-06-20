import pint
import enum


class UnitConverter:
    def __init__(self):
        self.sourceUnits = WorldUnitMapper()
        self.targetUnits = WorldUnitMapper()

    @staticmethod
    def _convert_units(length, source, target) :
        return length * target / source

    def to_target_length(self, length):
        return self.convert_units(length, self.sourceUnits.get_length_units(), self.targetUnits.get_length_units())

    def to_source_length(self, length):
        return self.convert_units(length, self.targetUnits.get_length_units(), self.sourceUnits.get_length_units())

    def to_target_weight(self, weight):
        return self.convert_units(weight, self.sourceUnits.get_weight_units(), self.targetUnits.get_weight_units())

    def to_source_weight(self, weight):
        return self.convert_units(weight, self.targetUnits.get_weight_units(), self.sourceUnits.get_weight_units())

    def _convert_coordinate(self, coordinatem, source, target):
        return "notImplemented"


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
