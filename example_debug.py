"""This file contains examples for debugging Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck import sensors
import cv2


def debug_vscode_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine Editor. Most people that use holodeck will not need this.

    This example uses a custom scenario, see 
    https://holodeck.readthedocs.io/en/latest/usage/examples/custom-scenarios.html

    Note: When launching Holodeck from the editor, press the down arrow next to "Play" and select
    "Standalone Game", otherwise the editor will lock up when the client stops ticking it.
    """

    config = {
    "name": "Multiagent",
    "world": "UrbanCity",
    "main_agent": "uav0",
    "agents":[
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    "rotation": [0.0, 0.0, 0.0],
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
                }
            ],
            "control_scheme": 0,
            "location": [0.0, 0.0, 0.0],
            "rotation": [0.0, 0.0, 0.0]
        },
        {
            "agent_name": "uav1",
            "agent_type": "UavAgent",
            "sensors": [
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
                }
            ],
            "control_scheme": 0,
            "location": [2.0, 0.0, 0.0],
            "rotation": [90.0, 0.0, 0.0]
        }
    ],

    "window_width":  1280,
    "window_height": 720
    }


    env = HolodeckEnvironment(scenario=config, start_world=False, verbose=False)
    command = [0, 0, 0, 5]
    
    for i in range(10):
        env.reset()
        env.act("uav0", [0,0,0,0])
        env.act("uav1", command)
        env.tick()
        env.tick()
        # env.set_state("uav0", [0, 0, 5], [0, 0, 0], [0, 0, 0], [0, 0, 0])
        # env.agents["boat0"].set_physics_state(pos, rot, [0,0,0],[0,0,0])
        # env.agents["uav0"].sensors["RGBCamera"].rotate([0, -90, 0])
        for _ in range(1000):
            state = env.tick()
            # pixels = state["RGBCamera"]

            # cv2.imshow("Camera Output", pixels[:, :, 0:3])
            # cv2.waitKey(1)
            #print(states["boat0"]["KeyPointsSensor"][0])


if __name__ == '__main__':
    debug_vscode_example()