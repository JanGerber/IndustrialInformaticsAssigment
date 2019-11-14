import json
import uuid

import requests


class Conveyor:

    def __init__(self, hostIP):
        self.conveyorID = uuid.uuid4()
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        print("New Conveyor initiated (" + str(self.conveyorID) + ")")

    def movePallet(self, zoneStart: int, zoneEnd: int):
        url = self.hostIP + self.baseService + "/TransZone" + str(zoneStart) + str(zoneEnd)
        r = requests.post(url, json={"destUrl": ""})
        if r.status_code == 202:
            print("Successful")
        else:
            print("Something went wrong!!")

    def getZoneStatus(self, zoneNumber: int):
        url = self.hostIP + self.baseService + "/Zone" + str(zoneNumber)
        r = requests.post(url, json={"destUrl": ""})

        reqMsg = json.loads(r.text)
        palletID = reqMsg["PalletID"]

        return palletID
