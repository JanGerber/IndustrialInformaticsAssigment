import logging
import uuid

import requests

from industrial_informatic_assigment.enum.phone_color import PhoneColor
from industrial_informatic_assigment.enum.phone_shape import PhoneShape
from industrial_informatic_assigment.exceptions.workstation_exception import WorkstationError


class Robot:
    def __init__(self, hostIP):
        self.robotID = uuid.uuid4()
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        logging.debug("Initialization: new robot  (" + str(self.robotID) + ")")

    def calibrateRobot(self):
        url = self.hostIP + self.baseService + "/Calibrate"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, json={}, headers=headers)

    def selectPen(self, color: PhoneColor):

        colorUrlValue = ""
        if color == PhoneColor.BLUE:
            colorUrlValue = "ChangePenBLUE"
        elif color == PhoneColor.GREEN:
            colorUrlValue = "ChangePenGREEN"
        elif color == PhoneColor.RED:
            colorUrlValue = "ChangePenRED"
        url = self.hostIP + self.baseService + "/" + colorUrlValue
        r = requests.post(url, json={"destUrl": ""})
        if r.status_code == 202:
            logging.info("Robot: select pen successful, color: " + str(color.name))
        else:
            logging.error(
                "Robot: select pen failure, color: " + str(color.name) + ", Status Code: " + str(r.status_code))
            raise WorkstationError("An error occurred when starting to change the pen.")

    def executeDrawing(self, shape: PhoneShape, color: PhoneColor):
        if color != self.getPenColor():
            logging.warning("Robot: wrong color selected")
        url = self.hostIP + self.baseService + "/" + shape.value
        r = requests.post(url, json={"destUrl": ""})
        if r.status_code == 202:
            logging.info("Robot: execute drawing successful, color: " + str(color.name))
        else:
            logging.error("Robot: execute drawing failure, color: " + str(color.name) + ", shape: " + str(
                shape.name) + " Status Code: " + str(r.status_code))
            raise WorkstationError("An error occurred when starting to execute the drawing.")

    def getPenColor(self) -> PhoneColor:
        logging.info("Robot: get pen color")
        url = self.hostIP + self.baseService + "/GetPenColor"
        r = requests.post(url, json={})
        logging.debug(r.json())
        response = r.json()
        if response == "red":
            return PhoneColor.RED
        if response == "green":
            return PhoneColor.GREEN
        if response == "blue":
            return PhoneColor.BLUE
        raise WorkstationError("An error has occurred while retrieving the pen color.")
