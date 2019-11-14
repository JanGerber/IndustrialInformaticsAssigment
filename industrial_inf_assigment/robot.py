import uuid

import requests

from industrial_inf_assigment.phone_color import PhoneColor
from industrial_inf_assigment.phone_shape import PhoneShape


class Robot:
    def __init__(self, hostIP):
        self.robotID = uuid.uuid4()
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        print("New robot initiated (" + str(self.robotID) + ")")

    def calibrateRobot(self):
        url = self.hostIP + self.baseService + "/Calibrate"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, json={}, headers=headers)

    def selectPen(self, color: PhoneColor):
        print("Select Pen")
        colorUrlValue = ""
        if color == PhoneColor.BLUE:
            colorUrlValue = "ChangePenBLUE"
        elif color == PhoneColor.GREEN:
            colorUrlValue = "ChangePenGREEN"
        elif color == PhoneColor.RED:
            colorUrlValue = "ChangePenRED"
        url = self.hostIP + self.baseService + "/" + colorUrlValue
        r = requests.post(url, json={"destUrl": ""})
        # TODO implement status code evaluation

    def executeDrawing(self, color: PhoneColor, shape: PhoneShape):
        if color != self.getPenColor():
            self.selectPen(color)
        url = self.hostIP + self.baseService + "/" + shape.value
        r = requests.post(url, json={"destUrl": ""})
        if r.status_code == 202:
            print("Successful")
        # TODO implement status code evaluation and return

    def getPenColor(self) -> PhoneColor:
        print("Get Pen color")
        url = self.hostIP + self.baseService + "/GetPenColor"
        r = requests.post(url, json={})

        return PhoneColor.RED  # TODO read data from request
