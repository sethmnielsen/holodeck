"""Definition of all of the sensor information"""
import json

import numpy as np
from holodeck.command import SetSensorEnabledCommand


class HolodeckSensor:
    """Base class for a sensor

    Args:
        client (:class:`~holodeck.holodeckclient.HolodeckClient`): Client attached to a sensor
        agent_name (:obj:`str`): Name of the agent
        name (:obj:`str`): Name of the sensor
    """
    def __init__(self, client, agent_name=None, name="DefaultSensor", config=None):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data",
                                                       self.data_shape, self.dtype)

        self.config = {} if config is None else config

    def set_sensor_enable(self, enable):
        """Enable or disable this sensor

        Args:
            enable (:obj:`bool`): State to set sensor to

        """
        command_to_send = SetSensorEnabledCommand(self.agent_name, self.name, enable)
        self._client.command_center.enqueue_command(command_to_send)

    @property
    def sensor_data(self):
        """Get the sensor data buffer

        Returns:
            :obj:`np.ndarray` of size :obj:`self.data_shape`: Current sensor data

        """
        return self._sensor_data_buffer

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype: Type of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            :obj:`tuple`: Sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class DistanceTask(HolodeckSensor):

    sensor_type = "DistanceTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class LocationTask(HolodeckSensor):

    sensor_type = "LocationTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class FollowTask(HolodeckSensor):

    sensor_type = "FollowTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class AvoidTask(HolodeckSensor):

    sensor_type = "AvoidTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class ViewportCapture(HolodeckSensor):
    sensor_type = "ViewportCapture"

    def __init__(self, client, agent_name, name="ViewportCapture", shape=(512, 512, 4)):
        """Represents a viewport capture.

        Args:
            shape (:obj:`tuple`): Dimensions of the capture
        """
        self.shape = shape
        super(ViewportCapture, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(HolodeckSensor):
    """Captures agent's view.

    The default capture resolution is 256x256x256x4, corresponding to the RGBA channels.
    The resolution can be increased, but will significantly impact performance.

    **Configuration**

    The ``configuration`` block (see :ref:`configuration-block`) accepts the following
    options:

    - ``CaptureWidth``: Width of captured image
    - ``CaptureHeight``: Height of captured image

    Args:
        shape (:obj:`tuple`): Dimensions of the capture

    """

    sensor_type = "RGBCamera"

    def __init__(self, client, agent_name, name="RGBCamera", width=256, height=256, config=None):

        self.config = {} if config is None else config

        if "CaptureHeight" in self.config:
            height = self.config["CaptureHeight"]

        if "CaptureWidth" in self.config:
            width = self.config["CaptureWidth"]


        self.shape = (height, width, 4)

        super(RGBCamera, self).__init__(client, agent_name, name=name, config=config)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(HolodeckSensor):
    """Gets the forward, right, and up vector for the agent.
    Returns a 2D numpy array of

    ::

       [ [forward_x, forward_y, forward_z],
         [right_x,   right_y,   right_z  ],
         [up_x,      up_y,      up_z     ] ]

    """

    sensor_type = "OrientationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(HolodeckSensor):
    """Inertial Measurement Unit sensor.

    Returns a 2D numpy array of

    ::

       [ [acceleration_x, acceleration_y, acceleration_z],
         [velocity_roll,  velocity_pitch, velocity_yaw]   ]

    """

    sensor_type = "IMUSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(HolodeckSensor):
    """Returns the state of the :class:`~holodeck.agents.AndroidAgent`'s joints in a
    94-length vector.

    See :ref:`android-joints` for the indexes into this vector.

    """

    sensor_type = "JointRotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class PressureSensor(HolodeckSensor):
    """For each joint on the :class:`~holodeck.agents.AndroidAgent`, returns the pressure on the
    joint.

    For each joint, returns ``[x_loc, y_loc, z_loc, force]``, in the order the joints are listed
    in :ref:`android-joints`.

    """

    sensor_type = "PressureSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]


class RelativeSkeletalPositionSensor(HolodeckSensor):
    """Gets the position of each bone in a skeletal mesh as a quaternion.

    Returns a numpy array of size (67, 4)
    """

    sensor_type = "RelativeSkeletalPositionSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(HolodeckSensor):
    """Gets the location of the agent in the world.

    Returns coordinates in ``[x, y, z]`` format (see :ref:`coordinate-system`)
    """

    sensor_type = "LocationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(HolodeckSensor):
    """Gets the rotation of the agent in the world.

    Returns ``[roll, pitch, yaw]`` (see :ref:`rotations`)
    """
    sensor_type = "RotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(HolodeckSensor):
    """Returns the x, y, and z velocity of the agent.
    
    """
    sensor_type = "VelocitySensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(HolodeckSensor):
    """Returns true if the agent is colliding with anything (including the ground).
    
    """

    sensor_type = "CollisionSensor"

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class SensorDefinition:
    """A class for new sensors and their parameters, to be used for adding new sensors.

    Args:
        agent_name (:obj:`str`): The name of the parent agent.
        sensor_name (:obj:`str`): The name of the sensor.
        sensor_type (:obj:`str` or :class:`HolodeckSensor`): The type of the sensor.
        socket (:obj:`str`, optional): The name of the socket to attach sensor to.
        location (Tuple of :obj:`float`, optional): ``[x, y, z]`` coordinates to place sensor
            relative to agent (or socket) (see :ref:`coordinate-system`).
        rotation (Tuple of :obj:`float`, optional): ``[roll, pitch, yaw]`` to rotate sensor
            relative to agent (see :ref:`rotations`)
        config (:obj:`dict`): Configuration dictionary for the sensor, to pass to engine
    """

    _sensor_keys_ = {"RGBCamera": RGBCamera,
                     "DistanceTask": DistanceTask,
                     "LocationTask": LocationTask,
                     "FollowTask": FollowTask,
                     "AvoidTask": AvoidTask,
                     "ViewportCapture": ViewportCapture,
                     "OrientationSensor": OrientationSensor,
                     "IMUSensor": IMUSensor,
                     "JointRotationSensor": JointRotationSensor,
                     "RelativeSkeletalPositionSensor": RelativeSkeletalPositionSensor,
                     "LocationSensor": LocationSensor,
                     "RotationSensor": RotationSensor,
                     "VelocitySensor": VelocitySensor,
                     "PressureSensor": PressureSensor,
                     "CollisionSensor": CollisionSensor}

    def get_config_json_string(self):
        """Gets the configuration dictionary as a string ready for transport

        Returns:
            (:obj:`str`): The configuration as an escaped json string

        """
        param_str = json.dumps(self.config)
        # Prepare configuration string for transport to the engine
        param_str = param_str.replace("\"", "\\\"")
        return param_str

    def __init__(self, agent_name, sensor_name, sensor_type, socket="",
                 location=(0, 0, 0), rotation=(0, 0, 0), config=None, existing=False):
        self.agent_name = agent_name
        self.sensor_name = sensor_name

        if isinstance(sensor_type, str):
            self.type = SensorDefinition._sensor_keys_[sensor_type]
        else:
            self.type = sensor_type

        self.socket = socket
        self.location = location
        self.rotation = rotation
        self.config = {} if config is None else config
        self.existing = existing


class SensorFactory:
    """Given a sensor definition, constructs the appropriate HolodeckSensor object.

    """
    @staticmethod
    def _default_name(sensor_class):
        return sensor_class.sensor_type

    @staticmethod
    def build_sensor(client, sensor_def):
        """Constructs a given sensor associated with client

        Args:
            client (:obj:`str`): Name of the agent this sensor is attached to
            sensor_def (:class:`SensorDefinition`): Sensor definition to construct

        Returns:

        """
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name,
                               sensor_def.sensor_name, config=sensor_def.config)
