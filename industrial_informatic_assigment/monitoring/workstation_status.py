from typing import List

from industrial_informatic_assigment.monitoring.status import Status


class WorkstationStatus:
    def __init__(self, zone1, zone2, zone3, zone4, zone5, robot):
        self.zone1 = zone1
        self.zone2 = zone2
        self.zone3 = zone3
        self.zone4 = zone4
        self.zone5 = zone5
        self.robot = robot
