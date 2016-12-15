import Holodeck.holodeck_agents as ha
import numpy as np
import json
import base64
import cv2

class HolodeckEnvironment:

    def __init__(self, agent_type, hostname="localhost", port=8989, agent_name="DefaultAgent",global_state_sensors={}):
        """

        :param agent_type: str()
        :param hostname:
        :param port:
        :param agent_name:
        """
        agents = {"UAV": ha.UAVAgent, "SPHERE": ha.SphereRobotAgent, "ANDROID": ha.AndroidAgent}
        if agent_type in agents.keys():
            agent = agents[agent_type]
        else:
            raise KeyError(agent_type + " is not a valid agent type")
        self.AGENT = agents[agent_type](hostname=hostname, port=port, agentName=agent_name,global_state_sensors=global_state_sensors).waitFor("Connect")
        self.agent_type = agent_type

        #default have simulator to pause every 1 frame
        self.AGENT.worldCommand().setAllowedTicksBetweenCommands(1).send()

        # self.HOSTNAME = hostname
        # self.PORT = port
        # self.AGENT_NAME = agent_name

    def get_action_dim(self):
        return self.AGENT.get_action_space_dim()

    def get_state_dim(self):
        return self.AGENT.get_state_space_dim()

    def reset(self):
        self.AGENT.worldCommand().restartLevel().send()

    def act(self, action):
        assert action.shape == self.get_action_dim()

        self.AGENT.act(action)

        state = self.AGENT.get_state()

        np_images = []
        if "CameraSensorArray2D" in state:
            sensor = json.loads(state["CameraSensorArray2D"])
            for obj in sensor:
                for camera,base64_image in obj.items():
                    img = base64.b64decode(base64_image)
                    
                    npimg = np.fromstring(img, dtype=np.uint8)
                    np_images.append(npimg)

        other_outputs = []
        if "Score" in state:
            other_outputs.append(state["Score"])

        if "Terminal" in state:
            other_outputs.append(state["Terminal"])

        if "RelativeSkeletalPositionSensor" in state:
            skel_arr = []
            skeletal_positions = json.loads(state["RelativeSkeletalPositionSensor"])
            for obj in skeletal_positions:
                skel_arr.append(obj["Quaternion"]["X"])
                skel_arr.append(obj["Quaternion"]["Y"])
                skel_arr.append(obj["Quaternion"]["Z"])
                skel_arr.append(obj["Quaternion"]["W"])
            other_outputs.append(skel_arr)

        if "JointRotationSensor" in state:
            joint_arr = []
            joint_rotations = json.loads(state["JointRotationSensor"])
            for obj in joint_rotations:
                joint_arr.append(obj)
            other_outputs.append(joint_arr)

        if "IMUSensor" in state:
            imu_arr = []
            imu_readings = json.loads(state["JointRotationSensor"])
            for obj in imu_readings:
                imu_arr.append(obj)
            other_outputs.append(imu_arr)

        # if "PressureSensor" in state:
        #     pressure_readings = json.loads(state["PressureSensor"])
        #     output["PressureSensor"] = state["PressureSensor"]

        output = np.array([np_images,other_outputs])
        print(output)

        return output