import uuid

from industrial_inf_assigment.conveyor import Conveyor
from industrial_inf_assigment.robot import Robot


class Workstation:

    def __init__(self, baseIp):
        self.orchestratorID = uuid.uuid4()
        self.robot = Robot(baseIp + ".1")
        self.conveyor = Conveyor(baseIp + ".2")
        print("New orchestrator initiated (" + str(self.orchestratorID) + ")")
