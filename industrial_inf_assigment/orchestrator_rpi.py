import logging
import time
import uuid

from industrial_inf_assigment.orchestrator_status import OrchestratorStatus
from industrial_inf_assigment.pallet import Pallet
from industrial_inf_assigment.pallet_status import PalletStatus
from industrial_inf_assigment.phone import Phone
from industrial_inf_assigment.status_code import StatusCode
from industrial_inf_assigment.workstation import Workstation
from industrial_inf_assigment.zone import Zone


class Orchestrator:

    def __init__(self, orchestratorStatus: OrchestratorStatus, workstation: Workstation):
        self.orchestratorID = uuid.uuid4()
        self.ws = workstation
        self.bufferOrder = []
        self.status = orchestratorStatus
        logging.debug("Initialization: new orchestrator  (" + str(self.orchestratorID) + ")")

    def runOrchestation(self):
        while True:

            self.testNextStepInZone1()
            self.testNextStepInZone2()
            self.testNextStepInZone3()
            self.testNextStepInZone4()
            self.printPalletInfos()
            self.testForWorking()
            time.sleep(5)

    def addNewOrder(self, phone: Phone):
        logging.info("Orchestrator: new phone added to order list")
        if self.ws.conveyor.getZoneStatus(Zone.Z1) == -1:
            logging.debug("Orchestrator: add to buffer 1")
            self.addOrderToBuffer(phone)
        elif self.testIfAnyPalletIsInZone(Zone.Z1):
            logging.debug("Orchestrator: add to buffer 1")
            self.addOrderToBuffer(phone)
        else:
            logging.debug("Orchestrator: add to pallet")
            self.addPhoneToPallet(phone)

    def addOrderToBuffer(self, phone: Phone):
        if len(self.bufferOrder) >= 2:
            logging.info("Orchestrator: max number of orders are already reached")
            return
        self.bufferOrder.append(phone)

    def penSelectedEndEvent(self):
        pallet = self.getPalletOnZone(Zone.Z2)
        pallet.status = PalletStatus.WAIT_FOR_MOVING

    def penSelectedStartEvent(self):
        pass

    def testIfAnyPalletIsInZone(self, zone: Zone) -> bool:
        if len(self.ws.pallets) > 0:
            for pallet in self.ws.pallets:
                if pallet.locationZone == zone:
                    return True
        return False

    def addPhoneToPallet(self, phone: Phone):
        pallet = Pallet(phone, self.ws, Zone.Z1)
        pallet.status = PalletStatus.WAIT_FOR_MOVING
        self.addPalletToWS(pallet)

    def addPalletToWS(self, pallet):
        if len(self.ws.pallets) >= 5:
            logging.warning("Orchestrator: there are already 5 pallets in the ws")
        self.ws.pallets.append(pallet)

    def drawingEndEvent(self):
        pallet = self.getPalletOnByStatus(PalletStatus.DRAWING)

        if not pallet.frameDone or not pallet.screenDone or not pallet.keyboardDone:
            pallet.status = PalletStatus.WAITING
            return

        pallet.status = PalletStatus.WAIT_FOR_MOVING

    def zone3ChangedEvent(self, palletId: int):
        if palletId == -1:
            return
        pallet = self.getPalletOnByStatus(PalletStatus.MOVING_TO_Z3)
        if pallet is None:
            return
        pallet.locationZone = Zone.Z3
        pallet.status = PalletStatus.WAITING

    def zone4ChangedEvent(self, palletId: int):
        if palletId == -1:
            return
        pallet = self.getPalletOnByStatus(PalletStatus.MOVING_TO_Z4)
        if pallet is None:
            return
        pallet.locationZone = Zone.Z4
        pallet.status = PalletStatus.WAITING

    def zone5ChangedEvent(self, palletId: int):
        if palletId == -1:
            pallet = self.getPalletOnByStatus(PalletStatus.WAIT_FOR_REMOVAL)
            if pallet is None:
                return
            self.ws.pallets.remove(pallet)
            return
        pallet = self.getPalletOnByStatus(PalletStatus.MOVING_TO_Z5)
        if pallet is None:
            return
        pallet.locationZone = Zone.Z5
        pallet.status = PalletStatus.WAIT_FOR_REMOVAL

    def testIfAnyPalletStatusIs(self, status: PalletStatus) -> bool:
        for pallet in self.ws.pallets:
            if pallet.status == status:
                return True
        return False

    def getPalletOnZone(self, zone: Zone) -> Pallet:
        for pallet in self.ws.pallets:
            if pallet.locationZone == zone:
                return pallet
        logging.error("Orchestrator: couldn't find pallet on zone: " + str(zone.name))

    def getPalletOnByStatus(self, status: PalletStatus):
        for pallet in self.ws.pallets:
            if pallet.status == status:
                return pallet
        logging.error("Orchestrator: couldn't find pallet with that status: " + str(status.name))

    def drawingStartEvent(self):
        pass

    def testNextStepInZone1(self):
        if not self.testIfAnyPalletIsInZone(Zone.Z1):
            return
        pallet = self.getPalletOnZone(Zone.Z1)
        if pallet.status == PalletStatus.MOVING_TO_Z2:
            return
        if not self.testIfAnyPalletIsInZone(Zone.Z2) and not self.testIfAnyPalletStatusIs(PalletStatus.MOVING_TO_Z2):
            logging.info("Orchestrator: move pallet from zone 1 to zone 2")
            pallet.status = PalletStatus.MOVING_TO_Z2
            self.ws.conveyor.movePallet(Zone.Z1, Zone.Z2)
            return
        if len(self.bufferOrder) == 0:
            return
        if not self.testIfAnyPalletIsInZone(Zone.Z4) and not self.testIfAnyPalletStatusIs(PalletStatus.MOVING_TO_Z4):
            logging.info("Orchestrator: move pallet from zone 1 to zone 4")
            pallet.status = PalletStatus.MOVING_TO_Z4
            self.ws.conveyor.movePallet(Zone.Z1, Zone.Z4)

    def testNextStepInZone2(self):
        if not self.testIfAnyPalletIsInZone(Zone.Z2):
            return
        pallet = self.getPalletOnZone(Zone.Z2)
        if pallet.status == PalletStatus.MOVING_TO_Z3 or pallet.status == PalletStatus.WAIT_PEN_CHANGE:
            return
        if pallet.status == PalletStatus.WAITING and not self.testIfAnyPalletIsInZone(Zone.Z3):
            color = self.ws.robot.getPenColor()
            if color != pallet.phone.color:
                logging.info("Orchestrator: change pen")
                pallet.status = PalletStatus.WAIT_PEN_CHANGE
                self.ws.robot.selectPen(pallet.phone.color)
        if pallet.status == PalletStatus.WAIT_FOR_MOVING and not self.testIfAnyPalletIsInZone(Zone.Z3):
            logging.info("Orchestrator: move pallet from zone 2 to zone 3")
            pallet.status = PalletStatus.MOVING_TO_Z3
            self.ws.conveyor.movePallet(Zone.Z2, Zone.Z3)

    def testNextStepInZone3(self):
        if not self.testIfAnyPalletIsInZone(Zone.Z3):
            return
        pallet = self.getPalletOnZone(Zone.Z3)
        if pallet.status == PalletStatus.MOVING_TO_Z4 or pallet.status == PalletStatus.DRAWING:
            return
        if pallet.status == PalletStatus.WAITING:
            if not pallet.frameDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.frameShape, pallet.phone.color)
                pallet.frameDone = True
            elif not pallet.screenDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.screenShape, pallet.phone.color)
                pallet.screenDone = True
            elif not pallet.keyboardDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.keyboardShape, pallet.phone.color)
                pallet.keyboardDone = True
            return
        if pallet.status == PalletStatus.WAIT_FOR_MOVING and not self.testIfAnyPalletIsInZone(
                Zone.Z5) and not self.testIfAnyPalletStatusIs(PalletStatus.MOVING_TO_Z5):
            logging.info("Orchestrator: move pallet from zone 3 to zone 5")
            pallet.status = PalletStatus.MOVING_TO_Z5
            self.ws.conveyor.movePallet(Zone.Z3, Zone.Z5)

    def testNextStepInZone4(self):
        if not self.testIfAnyPalletIsInZone(Zone.Z4):
            return
        pallet = self.getPalletOnZone(Zone.Z4)
        if pallet.status == PalletStatus.MOVING_TO_Z4:
            return
        if not self.testIfAnyPalletIsInZone(Zone.Z5) and not self.testIfAnyPalletStatusIs(PalletStatus.MOVING_TO_Z5):
            pallet.status = PalletStatus.MOVING_TO_Z5
            self.ws.conveyor.movePallet(Zone.Z4, Zone.Z5)

    def testNextStepInZone5(self):
        if not self.testIfAnyPalletIsInZone(Zone.Z5):
            return

    def zone2ChangedEvent(self, palletId: int):
        if palletId == -1:
            return
        pallet = self.getPalletOnByStatus(PalletStatus.MOVING_TO_Z2)
        if pallet is None:
            return
        pallet.locationZone = Zone.Z2
        pallet.status = PalletStatus.WAITING

    def zone1ChangedEvent(self, palletId: int):
        if palletId == -1:
            return
        if self.testIfAnyPalletIsInZone(Zone.Z1):
            return
        if len(self.bufferOrder) >= 1:
            self.addPhoneToPallet(self.bufferOrder.pop())

    def printPalletInfos(self):
        for p in self.ws.pallets:
            p.printPalletInfo()

    def testForWorking(self):
        for p in self.ws.pallets:
            if p.status is PalletStatus.WAIT_PEN_CHANGE or p.status is PalletStatus.MOVING_TO_Z2 or p.status is PalletStatus.MOVING_TO_Z3 or p.status is PalletStatus.MOVING_TO_Z4 or p.status is PalletStatus.MOVING_TO_Z5 or p.status is PalletStatus.DRAWING:
                self.status.changeColor(StatusCode.WORKING)
                return
        self.status.changeColor(StatusCode.IDLE)
