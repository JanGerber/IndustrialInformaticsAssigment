import datetime
import json
from typing import List

from industrial_informatic_assigment.enum.alarms import Alarms
from industrial_informatic_assigment.enum.conveyor_status import ConveyorStatus
from industrial_informatic_assigment.enum.events import Events
from industrial_informatic_assigment.enum.robot_status import RobotStatus
from industrial_informatic_assigment.monitoring.alarm import Alarm
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

    def getStatusOfZone(self, event: EventWS):
        status = []
        if event is None:
            status.append({"PalletID": "-"})
            status.append({"serverTime": "-"})
            status.append({"Status": ConveyorStatus.UNKNOWN.value})
        else:
            payload = json.loads(event.payload)
            status.append({"PalletID": payload["PalletID"]})
            status.append({"serverTime": str(event.serverTime)})
            if payload["PalletID"] == -1 or payload["PalletID"] == "-1":
                status.append({"Status": ConveyorStatus.FREE.value})
            else:
                status.append({"Status": ConveyorStatus.OCCUPIED.value})
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
        self.checkForPenChangeNotEnded(eventPenStart, eventPenEnd)
        self.checkForUnkownPosAfterZ1(eventZ1, eventZ2, eventZ4)
        self.checkForUnkownPosAfterZ2(eventZ2, eventZ3)
        self.checkForUnkownPosAfterZ3(eventZ3, eventZ5)
        self.checkForUnkownPosAfterZ4(eventZ4, eventZ5)
        self.checkForNotMovingZ1(eventZ1)
        self.checkForNotMovingZ2(eventZ2)
        self.checkForNotMovingZ3(eventZ3)
        self.checkForNotMovingZ4(eventZ4)
        self.checkForNotMovingZ5(eventZ5)

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
            statusList.append({"Status": RobotStatus.UNKNOWN.value})
            return statusList
        newest: EventWS = None
        for e in events:
            if newest is None:
                newest = e
                continue
            if e.serverTime > newest.serverTime:
                newest = e

        if newest.eventID == Events.PEN_CHANGE_STARTED.value:
            payload = json.loads(newest.payload)
            statusList.append({"PenColor": payload["PenColor"]})
            statusList.append({"Status": RobotStatus.PEN_CHANGE.value})
        elif newest.eventID == Events.PEN_CHANGE_ENDED.value:
            payload = json.loads(newest.payload)
            statusList.append({"PenColor": payload["PenColor"]})
            statusList.append({"Status": RobotStatus.IDLE.value})
        elif newest.eventID == Events.DRAW_END_EXECUTION.value:
            payload = json.loads(newest.payload)
            statusList.append({"Recipe": payload["Recipe"]})
            statusList.append({"PenColor": payload["PenColor"]})
            statusList.append({"Status": RobotStatus.IDLE.value})
        elif newest.eventID == Events.DRAW_START_EXECUTION.value:
            payload = json.loads(newest.payload)
            statusList.append({"Recipe": payload["Recipe"]})
            statusList.append({"PenColor": payload["PenColor"]})
            statusList.append({"Status": RobotStatus.DRAWING.value})
        else:
            statusList.append({"Status": RobotStatus.IDLE.value})
        statusList.append({"serverTime": str(newest.serverTime)})
        return statusList

    def checkForDrawingNotEnded(self, startDrawEvent: EventWS, endDrawEvent: EventWS):
        if startDrawEvent is None:
            return
        serverTime = datetime.datetime.now()
        timediff = int((serverTime - startDrawEvent.serverTime).total_seconds())
        if endDrawEvent is not None:
            if endDrawEvent.serverTime > startDrawEvent.serverTime or timediff < 120:
                return
        if self.alarmDAO.testAlarmExist(Alarms.DRAWING_NOT_ENDED, startDrawEvent.id):
            return
        description = "The drawing(" + str(startDrawEvent.payload) + ") started at " + str(
            startDrawEvent.serverTime) + " has not been finished yet."
        alarm = Alarm(Alarms.DRAWING_NOT_ENDED.name, description, serverTime, startDrawEvent.id)
        self.alarmDAO.insertAlarm(alarm)

    def checkForPenChangeNotEnded(self, eventPenStart: EventWS, eventPenEnd: EventWS):
        if eventPenStart is None:
            return
        serverTime = datetime.datetime.now()
        timediff = int((serverTime - eventPenStart.serverTime).total_seconds())
        if eventPenEnd is not None:
            if eventPenEnd.serverTime > eventPenEnd.serverTime or timediff < 60:
                return
        if self.alarmDAO.testAlarmExist(Alarms.PEN_CHANGE_NOT_ENDED, eventPenStart.id):
            return
        description = "The pen change(" + str(eventPenStart.payload) + ") started at " + str(
            eventPenStart.serverTime) + " has not been finished yet."
        alarm = Alarm(Alarms.PEN_CHANGE_NOT_ENDED.name, description, serverTime, eventPenStart.id)
        self.alarmDAO.insertAlarm(alarm)

    def checkForUnkownPosAfterZ1(self, eventZ1: EventWS, eventZ2: EventWS, eventZ4: EventWS):
        pass

    def checkForUnkownPosAfterZ2(self, eventZ2: EventWS, eventZ3: EventWS):
        pass

    def checkForUnkownPosAfterZ3(self, eventZ3: EventWS, eventZ5: EventWS):
        pass

    def checkForUnkownPosAfterZ4(self, eventZ4: EventWS, eventZ5: EventWS):
        pass

    def checkForNotMovingZ1(self, eventZ1: EventWS):
        pass

    def checkForNotMovingZ2(self, eventZ2: EventWS):
        pass

    def checkForNotMovingZ3(self, eventZ3: EventWS):
        pass

    def checkForNotMovingZ4(self, eventZ4: EventWS):
        pass

    def checkForNotMovingZ5(self, eventZ5: EventWS):
        pass

    def getAllAlarms(self):
        alarms = self.alarmDAO.getAllAlarms()
        for a in alarms:
            a["serverTime"] = str(
                a["serverTime"])  # FIXME vielleicht sollte man einfach ein richtiges Framework verwenden
        return alarms

    def getAllEvents(self):
        events = self.eventsDAO.get_all_events()
        for e in events:
            e["serverTime"] = str(
                e["serverTime"])  # FIXME vielleicht sollte man einfach ein richtiges Framework verwenden
        return events

    def getAllNewAlarms(self, alarmId):
        alarms = self.alarmDAO.getAllNewAlarms(alarmId)
        for a in alarms:
            a["serverTime"] = str(
                a["serverTime"])  # FIXME vielleicht sollte man einfach ein richtiges Framework verwenden
        return alarms
