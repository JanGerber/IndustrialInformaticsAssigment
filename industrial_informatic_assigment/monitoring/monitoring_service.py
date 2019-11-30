import json
from typing import List

from industrial_informatic_assigment.enum.events import Events
from industrial_informatic_assigment.monitoring import event_ws
from industrial_informatic_assigment.monitoring.event_ws import EventWS
from industrial_informatic_assigment.monitoring.monitoring_alarm_dao import MonitoringAlarmDAO
from industrial_informatic_assigment.monitoring.monitoring_event_dao import MonitoringEventDAO
from industrial_informatic_assigment.monitoring.workstation_status import WorkstationStatus


class MonitoringService:
    def __init__(self, daoEvents: MonitoringEventDAO, alarmDAO: MonitoringAlarmDAO):
        self.eventsDAO = daoEvents
        self.alarmDAO = alarmDAO

    def getStatusOfWS(self) -> WorkstationStatus:
        eventZ1 = self.eventsDAO.getLastEvent(Events.Z1_CHANGED)
        statusZ1 = self.getStatusOfZone(eventZ1)

        eventZ2 = self.eventsDAO.getLastEvent(Events.Z2_CHANGED)
        statusZ2 = self.getStatusOfZone(eventZ2)

        eventZ3 = self.eventsDAO.getLastEvent(Events.Z3_CHANGED)
        statusZ3 = self.getStatusOfZone(eventZ3)

        eventZ4 = self.eventsDAO.getLastEvent(Events.Z4_CHANGED)
        statusZ4 = self.getStatusOfZone(eventZ4)

        eventZ5 = self.eventsDAO.getLastEvent(Events.Z5_CHANGED)
        statusZ5 = self.getStatusOfZone(eventZ5)

        eventPenStart = self.eventsDAO.getLastEvent(Events.PEN_CHANGE_STARTED)
        eventPenEnd = self.eventsDAO.getLastEvent(Events.PEN_CHANGE_ENDED)
        eventDrawStart = self.eventsDAO.getLastEvent(Events.DRAW_START_EXECUTION)
        eventDrawEnd = self.eventsDAO.getLastEvent(Events.DRAW_END_EXECUTION)
        statusRobot = self.getStatusOfRobot(eventPenStart, eventPenEnd, eventDrawStart, eventDrawEnd)

        return WorkstationStatus(statusZ1, statusZ2, statusZ3, statusZ4, statusZ5, statusRobot)

    def getStatusOfZone(self, event: event_ws):
        if event is None:
            status = {"": ""}
        else:
            payload = json.loads("\"" + event.payload + "\"")
            status = {"PalletID": payload[0]}
        return status

    def checkForNewAlarms(self):
        eventZ1 = self.eventsDAO.getLastEvent(Events.Z1_CHANGED)
        eventZ2 = self.eventsDAO.getLastEvent(Events.Z2_CHANGED)
        eventZ3 = self.eventsDAO.getLastEvent(Events.Z3_CHANGED)
        eventZ4 = self.eventsDAO.getLastEvent(Events.Z4_CHANGED)
        eventZ5 = self.eventsDAO.getLastEvent(Events.Z5_CHANGED)
        eventPenStart = self.eventsDAO.getLastEvent(Events.PEN_CHANGE_STARTED)
        eventPenEnd = self.eventsDAO.getLastEvent(Events.PEN_CHANGE_ENDED)
        eventDrawStart = self.eventsDAO.getLastEvent(Events.DRAW_START_EXECUTION)
        eventDrawEnd = self.eventsDAO.getLastEvent(Events.DRAW_END_EXECUTION)
        self.checkForDrawingNotEnded(eventDrawStart, eventDrawEnd)
        self.checkForPenChangeNotEnded()
        self.checkForUnkownPosAfterZ1()
        self.checkForUnkownPosAfterZ2()
        self.checkForUnkownPosAfterZ3()
        self.checkForUnkownPosAfterZ4()
        self.checkForNotMovingZ1()
        self.checkForNotMovingZ2()
        self.checkForNotMovingZ3()
        self.checkForNotMovingZ4()
        self.checkForNotMovingZ5()

    def getStatusOfRobot(self, eventPenStart: EventWS, eventPenEnd: EventWS, eventDrawStart: EventWS,
                         eventDrawEnd: EventWS):
        events: List[EventWS] = []
        statusList = []
        if eventPenStart is not None:
            events.append(eventPenStart)
        if eventPenEnd is not None:
            events.append(eventPenEnd)
        if eventDrawStart is not None:
            events.append(eventDrawStart)
        if eventDrawEnd is not None:
            events.append(eventDrawEnd)
        if len(events) == 0:
            return statusList
        newest: EventWS = None
        for e in events:
            if newest is None:
                newest = e
                continue
            if e.serverTime > newest.serverTime:
                newest = e

        if newest.eventID == Events.PEN_CHANGE_STARTED.value or newest.eventID == Events.PEN_CHANGE_ENDED.value:
            payload = json.loads(newest.payload)
            statusList.append({"PenColor": payload})
        elif newest.eventID == Events.DRAW_END_EXECUTION.value or newest.eventID == Events.DRAW_START_EXECUTION.value:
            payload = json.loads("\"" + newest.payload + "\"")
            statusList.append({"Recipe": payload["Recipe"]})
            statusList.append({"PenColor": payload["PenColor"]})
        return statusList

    def checkForDrawingNotEnded(self, startDrawEvent, endDrawEvent):
        pass

    def checkForPenChangeNotEnded(self):
        pass

    def checkForUnkownPosAfterZ1(self):
        pass

    def checkForUnkownPosAfterZ2(self):
        pass

    def checkForUnkownPosAfterZ3(self):
        pass

    def checkForUnkownPosAfterZ4(self):
        pass

    def checkForNotMovingZ1(self):
        pass

    def checkForNotMovingZ2(self):
        pass

    def checkForNotMovingZ3(self):
        pass

    def checkForNotMovingZ4(self):
        pass

    def checkForNotMovingZ5(self):
        pass

    def getAllAlarms(self):
        return self.alarmDAO.getAllAlarms()
