import uuid


class Conveyor:

    def __init__(self, hostIP):
        self.conveyorID = uuid.uuid4()
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        print("New Conveyor initiated (" + str(self.robotID) + ")")
