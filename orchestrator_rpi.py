import uuid

from industrial_inf_assigment.phone import Phone


class Orchestrator:

    def __init__(self):
        self.orchestratorID = uuid.uuid4()
        self.bufferOrder = []
        print("New orchestrator initiated (" + str(self.orchestratorID) + ")")

    def addNewOrder(self, phone: Phone):
        print("New Phone Added to Orch")

    def addOrderToBuffer(self, phone: Phone):
        if self.bufferOrder.count() >= 2:
            return
        self.bufferOrder.append(phone)
