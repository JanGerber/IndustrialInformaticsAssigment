import logging
import uuid

from enum.pallet_status import PalletStatus
from workstation.workstation import Workstation
from workstation.phone import Phone
from enum.zone import Zone


class Pallet:

    def __init__(self, phone: Phone, locationWS: Workstation, locationZone: Zone):
        self.palletID = uuid.uuid4()
        self.phone = phone
        self.locationWS = locationWS
        self.locationZone = locationZone
        self.frameDone = False
        self.screenDone = False
        self.keyboardDone = False
        self.status = PalletStatus.WAITING
        logging.debug("Initialization: new pallet  (" + str(self.palletID) + ")")

    def printPalletInfo(self):
        logging.info(
            "Pallet: \tpalletID:" + str(self.palletID) + " Zone: " + str(self.locationZone) + " Status: " + str(
                self.status.name))
