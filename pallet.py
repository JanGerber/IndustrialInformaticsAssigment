import uuid

from industrial_inf_assigment.phone import Phone
from industrial_inf_assigment.workstation import Workstation
from industrial_inf_assigment.zone import Zone


class Pallet:

    def __init__(self, phone: Phone, locationWS: Workstation, locationZone: Zone):
        self.palletID = uuid.uuid4()
        self.phone = phone
        self.locationWS = locationWS
        self.locationZone = locationZone
        print("New pallet initiated (" + str(self.palletID) + ")")

    def printPalletInfo(self):
        print("\tPalletID:" + str(self.palletID))
