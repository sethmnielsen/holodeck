"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck import sensors
import cv2
import time

def uav_example():
    """A basic example of how to use the UAV agent."""
    env = holodeck.make("UrbanCity-MaxDistance")
    env.set_render_quality(3)

    # This line can be used to change the control scheme for an agent
    # env.agents["uav0"].set_control_scheme(ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

    for i in range(10):
        env.reset()

        # This command tells the UAV to not roll or pitch, but to constantly yaw left at 10m altitude.
        command = np.array([0, 0, 0, 1000])
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)
            # To access specific sensor data:
            pixels = state["RGBCamera"]
            velocity = state["VelocitySensor"]
            # For a full list of sensors the UAV has, consult the configuration file "InfiniteForest-MaxDistance.json"

    # You can control the AgentFollower camera (what you see) by pressing V to toggle spectator
    # mode. This detaches the camera and allows you to move freely about the world.
    # You can also press C to snap to the location of the camera to see the world from the perspective of the
    # agent. See the Controls section of the ReadMe for more details.

def uav_cam_rotate():
    env = holodeck.make('UrbanCity-RGBCam')
    env.reset()

    cmd0 = [0, 0, 0, 100]
    env.act("uav0", cmd0)

    uav = env.agents['uav0']
    ang = [0,-45, 0]  # roll, pitch, yaw of camera in body frame (0,0,0 is pointing forward) [degrees]
    uav.sensors['RGBCamera'].rotate(ang)

    cv2.namedWindow('Camera Output')
    cv2.moveWindow('Camera Output', 500, 500)

    for _ in range(1000):
        state = env.tick()

        pixels = state['RGBCamera']
        cv2.imshow('Camera Output', pixels[:, :, :3])
        cv2.waitKey(1)

    cv2.destroyAllWindows()


def boat_example():
    """A basic example of using the ocean world"""
    env = holodeck.make("Ocean-BoatLanding")

    cmd0 = np.array([0, 0, 0, 10])
    cmd1 = np.array([0, 10]) # direction in degrees, speed
    for i in range(5):
        env.reset()
        env.tick()

        # The boat only needs to be told the command once
        env.act("uav0", cmd0)
        env.act("boat0", cmd1)

        # env.agents['uav0'].uav.set_physics_state(pos, att, vel, omg)
        # env.agents['boat0'].uav.set_physics_state(pos, att, vel, omg)
        states = None

        # Wave height, wave intensity, wind direction. 1-12, 1-6, 0-360
        env.send_world_command("SetOceanState", num_params=[10, 30, 0])

        # This will immediately set the rotation, there is no smooth transition
        # env.rotate_sensor("uav0", "RGBCamera", [0, -90, 0])

        #  Aruco code is on by default
        # env.send_world_command("DisableArucoCode")

        cv2.namedWindow("Camera Output")
        cv2.moveWindow("Camera Output", 500, 500)

        for _ in range(1000):
            states = env.tick()
            # boatstate = states["boat0"]
            # print(boatstate["Stern"])
            # print(boatstate["Bow"])
            # print(boatstate["Port"])
            # print(boatstate["StarBoard"])
            # print(boatstate["LandingFrontLeft"])
            # print(boatstate["LandingFrontRight"])
            # print(boatstate["LandingBackLeft"])
            # print(boatstate["LandingBackRight"])

            pixels = states['uav0'][holodeck.sensors.RGBCamera.sensor_type]
            cv2.imshow("Camera Output", pixels[:, :, 0:3])
            cv2.waitKey(1)

        cv2.destroyAllWindows()

def sphere_example():
    """A basic example of how to use the sphere agent."""
    env = holodeck.make("MazeWorld-FinishMazeSphere")

    # This command is to constantly rotate to the right
    command = 2
    for i in range(10):
        env.reset()
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the sphere robot has, view the README


def android_example():
    """A basic example of how to use the android agent."""
    env = holodeck.make("AndroidPlayground-MaxDistance")

    # The Android's command is a 94 length vector representing torques to be applied at each of his joints
    command = np.ones(94) * 10
    for i in range(10):
        env.reset()
        for j in range(1000):
            if j % 50 == 0:
                command *= -1

            state, reward, terminal, _ = env.step(command)
            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the android has, view the README


def multi_agent_example():
    """A basic example of using multiple agents"""
    env = holodeck.make("CyberPunkCity-SethTest")

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([10, 0, 0])
    for i in range(10):
        env.reset()
        env.tick()
        env.act("uav0", cmd0)
        env.act("nav0", cmd1)
        for _ in range(1000):
            states = env.tick()

            pixels = states["uav0"]["RGBCamera"]
            location = states["uav0"]["LocationSensor"]

            task = states["uav0"]["FollowTask"]
            reward = task[0]
            terminal = task[1]

def world_command_examples():
    """A few examples to showcase commands for manipulating the worlds."""
    env = holodeck.make("Ocean-BoatLanding")

    # This is the unaltered MazeWorld
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_day_time_command sets the hour between 0 and 23 (military time). This example sets it to 6 AM.
    env.weather.set_day_time(6)
    for _ in range(300):
        _ = env.tick()
    env.reset()  # reset() undoes all alterations to the world

    # The start_day_cycle command starts rotating the sun to emulate day cycles.
    # The parameter sets the day length in minutes.
    env.weather.start_day_cycle(5)
    for _ in range(1500):
        _ = env.tick()
    env.reset()

    # The set_fog_density changes the density of the fog in the world. 1 is the maximum density.
    env.weather.set_fog_density(.25)
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_weather_command changes the weather in the world. The two available options are "rain" and "cloudy".
    # The rainfall particle system is attached to the agent, so the rain particles will only be found around each agent.
    # Every world is clear by default.
    env.weather.set_weather("rain")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.weather.set_weather("cloudy")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.move_viewport([1000, 1000, 1000], [0, 0, 0])
    for _ in range(500):
        _ = env.tick()
    env.reset()



def editor_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine Editor. Most people that use holodeck will not need this.

    This example uses a custom scenario, see
    https://holodeck.readthedocs.io/en/latest/usage/examples/custom-scenarios.html

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """

    config = {
        "name": "BoatLanding",
        "world": "Ocean",
        "main_agent": "uav0",
        "agents": [
            {
                "agent_name": "uav0",
                "agent_type": "UavAgent",
                "sensors": [
                    {
                        "sensor_type": "RGBCamera",
                        "socket": "CameraSocket",
                        "rotation": [0.0, 0.0, 0.0],
                        "configuration": {
                            "CaptureWidth": 640,
                            "CaptureHeight": 480
                        }
                    },
                    {
                        "sensor_type": "LocationSensor"
                    },
                    {
                        "sensor_type": "OrientationSensor"
                    },
                    {
                        "sensor_type": "RotationSensor"
                    },
                    {
                        "sensor_type": "VelocitySensor"
                    },
                    {
                        "sensor_type": "CollisionSensor"
                    },
                    {
                        "sensor_type": "IMUSensor"
                    }
                ],
                "control_scheme": 0,
                "location": [0.0, 0.0, 5.5],
                "rotation": [0.0, 0.0, 0.0]
            },
            {
                "agent_name": "boat0",
                "agent_type": "BoatAgent",
                "existing": True,
                "sensors": [
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "Bow",
                        "socket": "Bow"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "Stern",
                        "socket": "Stern"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "Port",
                        "socket": "Port"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "StarBoard",
                        "socket": "StarBoard"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "LandingFrontLeft",
                        "socket": "LandingFrontLeft"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "LandingFrontRight",
                        "socket": "LandingFrontRight"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "LandingBackLeft",
                        "socket": "LandingBackLeft"
                    },
                    {
                        "sensor_type": "LocationSensor",
                        "sensor_name": "LandingBackRight",
                        "socket": "LandingBackRight"
                    }
                ],
                "control_scheme": 0,
                "location": [20.0, 0.0, 5.0],
                "rotation": [90.0, 0.0, 0.0]
            }
        ]
    }

    env = HolodeckEnvironment(scenario=config, start_world=False, verbose=True)
    command = [0, 0, 0, 55]
    for i in range(100):
        env.reset()
        # env.act("uav0", command)
        psi = 0
        env.act("boat0", [psi,-2])
        _ = env.tick()
        _ = env.tick()
        pos = np.array([20, 0, 0])
        rot = np.array([0, 0, psi])
        _ = env.tick()
        # env.set_state("uav0", [0, 0, 5], [0, 0, 0], [0, 0, 0], [0, 0, 0])
        env.agents["boat0"].set_physics_state(pos, rot, [0,0,0],[0,0,0])
        env.send_world_command("SetOceanState", [3, 3, 0])
        # env.agents["uav0"].sensors["RGBCamera"].rotate([0, -90, 0])
        for _ in range(10000):
            state = env.tick()
            # time.sleep(0.1)
            pixels = state['uav0']["RGBCamera"]

            # cv2.imshow("Camera Output", pixels[:, :, 0:3])
            # cv2.waitKey(1)
            # print(states["boat0"]["KeyPointsSensor"][0])


def editor_multi_agent_example():
    """This editor example shows how to interact with holodeck worlds that have multiple agents.
    This is specifically for when working with UE4 directly and not a prebuilt binary.

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """
    config = {
        "name": "test_handagent",
        "world": "TestWorld",
        "main_agent": "hand0",
        "agents": [
            {
                "agent_name": "uav0",
                "agent_type": "UavAgent",
                "sensors": [
                ],
                "control_scheme": 1,
                "location": [0, 0, 1]
            },
            {
                "agent_name": "uav1",
                "agent_type": "UavAgent",
                "sensors": [
                ],
                "control_scheme": 1,
                "location": [0, 0, 5]
            }
        ]
    }

    env = HolodeckEnvironment(scenario=config, start_world=False)

    for i in range(10):
        env.reset()
        env.act("boat0", [2, 3])
        env.send_world_command("SetOceanState", num_params=[3, 3, 90])
        # env.rotate_sensor("uav0", "RGBCamera", [-90, 0, 0])
        # env.send_world_command("DisableArucoCode")
        env.set_state("uav0", [100, 100, 100], [0, 0, 180], [0, 0, 0], [0, 0, 0])
        for _ in range(100):
            states = env.tick()

        states = env.tick()
        pixels = states['uav0']["RGBCamera"]
        # cv2.namedWindow("Camera Output")
        # cv2.moveWindow("Camera Output", 500, 500)
        # cv2.imshow("Camera Output", pixels[:, :, 0:3])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def editor_infforest_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine Editor. Most people that use holodeck will not need this.

    This example uses a custom scenario, see
    https://holodeck.readthedocs.io/en/latest/usage/examples/custom-scenarios.html

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """

    config = {
        "name": "MaxDistance",
        "world": "InfiniteForest",
        "main_agent": "uav0",
        "agents":[
            {
                "agent_name": "uav0",
                "agent_type": "UavAgent",
                "sensors": [
                    {
                        "sensor_type": "RGBCamera",
                        "socket": "CameraSocket",
                        "configuration": {
                            "CaptureHeight": 480,
                            "CaptureWidth": 640
                        }
                    },
                    {
                        "sensor_type": "LocationSensor"
                    },
                    {
                        "sensor_type": "RotationSensor"
                    },
                    {
                        "sensor_type": "OrientationSensor"
                    },
                    {
                        "sensor_type": "VelocitySensor"
                    },
                    {
                        "sensor_type": "CollisionSensor"
                    },
                    {
                        "sensor_type": "IMUSensor"
                    },
                    {
                        "sensor_type": "AbuseSensor"
                    },
                    {
                        "sensor_type": "RangeFinderSensor",
                        "configuration": {
                            "LaserCount": 5
                        }
                    },
                    {
                        "sensor_type": "DistanceTask",
                        "configuration": {
                            "Interval": 5,
                            "GoalDistance": 1000,
                            "MaximizeDistance": True
                        }
                    }
                ],
                "control_scheme": 0,
                "location": [0.0, 0.0, 0.5],
                "rotation": [0.0, 0.0, 0.0]
            }
        ],

        "window_width":  1280,
        "window_height": 720
    }

    env = HolodeckEnvironment(scenario=config, start_world=False, verbose=True)
    command = [0, 0, 0, 0]
    for i in range(10):
        env.reset()
        env.act("uav0", command)
        _ = env.tick()
        _ = env.tick()
        # env.set_state("uav0", [0, 0, 5], [0, 0, 0], [0, 0, 0], [0, 0, 0])
        env.agents["uav0"].sensors["RGBCamera"].rotate([0, -90, 0])
        for _ in range(1000):
            state = env.tick()
            pixels = state["RGBCamera"]

            cv2.imshow("Camera Output", pixels[:, :, 0:3])
            cv2.waitKey(1)
            #print(states["boat0"]["KeyPointsSensor"][0])



if __name__ == "__main__":

    # uav_example()
    # uav_cam_rotate()
    editor_example()
    # editor_infforest_example()
