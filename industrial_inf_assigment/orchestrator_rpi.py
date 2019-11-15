import logging
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
        logging.debug("Initialization: new orchestrator  (" + str(self.orchestratorID) + ")")

    def runOrchestation(self):
        while True:
            time.sleep(20)
            logging.info("Orchestrator: orchestrate")


    def addNewOrder(self, phone: Phone):
        logging.info("Orchestrator: new phone added to order list")

    def addOrderToBuffer(self, phone: Phone):
        if self.bufferOrder.count() >= 2:
            return
        self.bufferOrder.append(phone)

    def penSelectedEndEvent(self):
        self.status.changeColor(StatusCode.IDLE)

    def penSelectedStartEvent(self):
        self.status.changeColor(StatusCode.WORKING)
