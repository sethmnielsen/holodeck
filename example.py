"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors


def multi_agent_example():
    """A basic example of using multiple agents"""
    env = holodeck.make("Ocean")

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = 10
    for i in range(10):
        env.reset()

        env.act("uav0", cmd0)
        env.act("boat0", cmd1)
        env.set_ocean_state(1, 1, 1)

        env.set_ocean_state(1, 1, 0)
        # env.set_day_time(0)

        for _ in range(1000):
            states = env.tick()


def world_command_examples():
    """A few examples to showcase commands for manipulating the worlds."""
    env = holodeck.make("MazeWorld")

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
    in the Unreal Engine. Most people that use holodeck will not need this.
    """
    sensors = [Sensors.LOCATION_SENSOR, Sensors.KEY_POINTS_SENSOR]
    boat = AgentDefinition("boat0", agents.BoatAgent, sensors)

    agent_definitions = [
        AgentDefinition("uav0", agents.UavAgent, [Sensors.PIXEL_CAMERA, Sensors.LOCATION_SENSOR]),
        boat
    ]

    env = HolodeckEnvironment(agent_definitions, start_world=False)
    command = np.array([20])
    _ = env.step(command)
    env.set_day_time(8)

    wave_intensity, wave_size, wave_direction = 13, 1, 0
    print("hello")
    for i in range(10):
        env.reset()
        # env.set_weather("rain")
        env.set_ocean_state(13, 1, 0)
        env.act("uav0", [0, 0, 0, 0])
        env.act("boat0", 20)
        states = env.tick()

        for _ in range(10000):
            states = env.tick()
            print(states["boat0"][Sensors.LOCATION_SENSOR][0])


if __name__ == "__main__":
    # if 'DefaultWorlds' not in holodeck.installed_packages():
    #     holodeck.install("DefaultWorlds")
    #     print(holodeck.package_info("DefaultWorlds"))
    multi_agent_example()
