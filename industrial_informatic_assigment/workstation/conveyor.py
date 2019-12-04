import logging
import uuid
from json import JSONDecodeError

import requests

from industrial_informatic_assigment.enum.zone import Zone
from industrial_informatic_assigment.exceptions.workstation_exception import WorkstationError


class Conveyor:

    def __init__(self, hostIP):
        self.conveyorID = uuid.uuid4()
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        logging.debug("Initialization: new conveyor  (" + str(self.conveyorID) + ")")

    def movePallet(self, zoneStart: Zone, zoneEnd: Zone):
        url = self.hostIP + self.baseService + "/TransZone" + str(zoneStart.value) + str(zoneEnd.value)
        r = requests.post(url, json={"destUrl": ""})
        if r.status_code == 202:
            logging.debug(
                "Conveyor: move pallet successful (Z" + str(zoneStart.value) + " to " + str(zoneEnd.value) + ")")
        else:
            logging.error(
                "Conveyor: move pallet error (Z" + str(zoneStart.value) + " to " + str(
                    zoneEnd.value) + ") Status Code: " + str(
                    r.status_code))
            raise WorkstationError("An error occurred when trying to move the pallet to the next zone.")

    def getZoneStatus(self, zone: Zone):
        url = self.hostIP + self.baseService + "/Z" + str(zone.value)
        r = None
        if zone == Zone.Z1:
            r = requests.get(url, json={"destUrl": ""})
        else:
            r = requests.post(url, json={"destUrl": ""})
        if r.status_code != 200:
            logging.error("Conveyor: get zone status error (Z" + str(zone.value) + ")")
            raise WorkstationError("An error occurred when trying to move the pallet to the next zone.")

        reqMsg = r.json()
        palletID = reqMsg["PalletID"]

        return palletID
