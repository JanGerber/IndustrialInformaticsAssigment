class Pallet:

    def __init__(self, palletID, partDescription):
        self.palletID = palletID
        self.partDescription = partDescription
        print("New pallet initiated (" + str(self.palletID) + ")")

    def printPalletInfo(self):
        print("\tPalletID:" + str(self.palletID) + " \tPartDescription: " + self.partDescription)
