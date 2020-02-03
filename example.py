"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck import sensors
import cv2


def boat_example():
    """A basic example of using the ocean world"""
    env = holodeck.make("Ocean-BoatLanding")

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([90, 10]) # direction in degrees, speed
    for i in range(5):
        env.reset()
        env.tick()

        # The boat only needs to be told the command once
        env.act("boat0", cmd1)
        states = None

        # Wave height, wave intensity, wind direction. 1-12, 1-6, 0-360
        env.send_world_command("SetOceanState", num_params=[11, 6, 90])

        # This will immediately set the rotation, there is no smooth transition
        env.rotate_sensor("uav0", "RGBCamera", [0, -90, 0])

        #  Aruco code is on by default
        env.send_world_command("DisableArucoCode")


        for _ in range(1000):
            states = env.tick()
            boatstate = states["boat0"]
            print(boatstate["Stern"])
            print(boatstate["Bow"])
            print(boatstate["Port"])
            print(boatstate["StarBoard"])
            print(boatstate["LandingFrontLeft"])
            print(boatstate["LandingFrontRight"])
            print(boatstate["LandingBackLeft"])
            print(boatstate["LandingBackRight"])

        # Print out the final frame
        pixels = states['uav0'][holodeck.sensors.RGBCamera.sensor_type]
        cv2.namedWindow("Camera Output")
        cv2.moveWindow("Camera Output", 500, 500)
        cv2.imshow("Camera Output", pixels[:, :, 0:3])
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def world_command_examples():
    """A few examples to showcase commands for manipulating the worlds."""
    env = holodeck.make("Ocean-BoatLanding")

    # This is the unaltered MazeWorld
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_day_time_command sets the hour between 0 and 23 (military time). This example sets it to 6 AM.
    env.set_day_time(6)
    for _ in range(300):
        _ = env.tick()
    env.reset()  # reset() undoes all alterations to the world

    # The start_day_cycle command starts rotating the sun to emulate day cycles.
    # The parameter sets the day length in minutes.
    env.start_day_cycle(5)
    for _ in range(1500):
        _ = env.tick()
    env.reset()

    # The set_fog_density changes the density of the fog in the world. 1 is the maximum density.
    env.set_fog_density(.25)
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_weather_command changes the weather in the world. The two available options are "rain" and "cloudy".
    # The rainfall particle system is attached to the agent, so the rain particles will only be found around each agent.
    # Every world is clear by default.
    env.set_weather("rain")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.set_weather("cloudy")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.teleport_camera([1000, 1000, 1000], [0, 0, 0])
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
        "name": "test",
        "world": "TestWorld",
        "main_agent": "uav0",
        "agents": [
            {
                "agent_name": "uav0",
                "agent_type": "UavAgent",
                "sensors": [
                    {
                        "sensor_type": "LocationSensor",
                    },
                    {
                        "sensor_type": "VelocitySensor"
                    },
                    {
                        "sensor_type": "RGBCamera"
                    }
                ],
                "control_scheme": 1,
                "location": [0, 0, 1]
            }
        ]
    }

    env = HolodeckEnvironment(scenario=config, start_world=False)
    command = [0, 0, 10, 50]

    wave_intensity, wave_size, wave_direction = 13, 1, 0
    for i in range(10):
        env.reset()
        env.set_aruco_code(False)
        #env.act("uav0", [0, 0, 0, 0])
        #env.act("boat0", 20)
        _ = env.tick()
        #env.teleport("boat0", np.array([0, 0, 0]), [0, 0, 0])
        env.set_state("uav0", [10, 0, 5000], [0, 0, 90], [0, 0, 0], [0, 0, 10000])
        for _ in range(400):
            states = env.tick()
            #print(states["boat0"]["KeyPointsSensor"][0])


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


if __name__ == "__main__":

    boat_example()
