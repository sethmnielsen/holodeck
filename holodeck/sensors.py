"""Definition of all of the sensor information"""
import numpy as np
from holodeck.sensors import *


class SensorDef(object):

    def __init__(self, sensor_name, sensor_type):
        self.name = sensor_name
        self.type = sensor_type


class SensorFactory(object):

    __sensor_keys__ = {"RGBCamera": RGBCamera,
                       RGBCamera: RGBCamera}

    @staticmethod
    def build_sensor(client, sensor_def):
        return SensorFactory.__sensor_keys__[sensor_def.type](client, sensor_def.name)


class Sensor(object):

    def __init__(self, client, name="DefaultSensor"):
        self.name = name
        self._client = client

        self._on_bool_buffer = self._client.malloc(name + "_teleport_flag", [1], np.uint8)
        self._sensor_data_buffer = self._client.malloc(name, self.data_shape, self.dtype)

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            tuple representing sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class Terminal(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class Reward(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [1]


class ViewportCapture(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(512, 512, 4)):
        super(ViewportCapture, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(256, 256, 4)):
        super(RGBCamera, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]
