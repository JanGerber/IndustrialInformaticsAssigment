import time
import uuid

from industrial_inf_assigment.orchestrator_status import OrchestratorStatus
from industrial_inf_assigment.phone import Phone
from industrial_inf_assigment.status_code import StatusCode


class Orchestrator():

    def __init__(self, orchestratorStatus: OrchestratorStatus):
        self.orchestratorID = uuid.uuid4()
        self.bufferOrder = []
        self.status = orchestratorStatus
        print("New orchestrator initiated (" + str(self.orchestratorID) + ")")

    def runOrchestation(self):
        while True:
            time.sleep(20)
            print("Orchestration")


    def addNewOrder(self, phone: Phone):
        print("New Phone Added to Orch")

    def addOrderToBuffer(self, phone: Phone):
        if self.bufferOrder.count() >= 2:
            return
        self.bufferOrder.append(phone)

    def penSelectedEndEvent(self):
        print("End Event Change Pen")
        self.status.changeColor(StatusCode.IDLE)

    def penSelectedStartEvent(self):
        print("Start Change Pen")
        self.status.changeColor(StatusCode.WORKING)
