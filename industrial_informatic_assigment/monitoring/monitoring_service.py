import datetime
import json
import logging
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
        self.checkForUnknownPosAfterZ1(eventZ1, eventZ2, eventZ4)
        self.checkForUnknownPosAfterZ2(eventZ2, eventZ3)
        self.checkForUnknownPosAfterZ3(eventZ3, eventZ5)
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

    def checkForUnknownPosAfterZ1(self, eventZ1: EventWS, eventZ2: EventWS, eventZ4: EventWS):
        if eventZ1 is None:
            return
        payloadZ1 = json.loads(eventZ1.payload)
        palletIdZ1 = payloadZ1["PalletID"]
        if str(palletIdZ1) != "-1":
            return
        serverTime = datetime.datetime.now()
        if eventZ2 is not None:
            timediff = int((serverTime - eventZ1.serverTime).total_seconds())
            if eventZ1.serverTime < eventZ2.serverTime or timediff < 20:
                return
        if eventZ4 is not None:
            timediff = int((serverTime - eventZ4.serverTime).total_seconds())
            if eventZ1.serverTime < eventZ4.serverTime or timediff < 20:
                return

        if self.alarmDAO.testAlarmExist(Alarms.UNKNOWN_POS_AFTER_Z1, eventZ1.id):
            return
        description = "The moving from Zone 1 to Zone 2/4 has not been finished yet. (started at: " + str(
            eventZ1.serverTime) + ")"
        alarm = Alarm(Alarms.UNKNOWN_POS_AFTER_Z1.name, description, serverTime, eventZ1.id)
        self.alarmDAO.insertAlarm(alarm)

    def checkForUnknownPosAfterZ2(self, eventZ2: EventWS, eventZ3: EventWS):
        if eventZ2 is None:
            return
        payloadZ1 = json.loads(eventZ2.payload)
        palletIdZ1 = payloadZ1["PalletID"]
        if str(palletIdZ1) != "-1":
            return
        serverTime = datetime.datetime.now()
        if eventZ3 is not None:
            timediff = int((serverTime - eventZ2.serverTime).total_seconds())
            if eventZ2.serverTime < eventZ3.serverTime or timediff < 20:
                return

        if self.alarmDAO.testAlarmExist(Alarms.UNKNOWN_POS_AFTER_Z2, eventZ2.id):
            return
        description = "The moving from Zone 2 to Zone 3 has not been finished yet. (started at: " + str(
            eventZ2.serverTime) + ")"
        alarm = Alarm(Alarms.UNKNOWN_POS_AFTER_Z1.name, description, serverTime, eventZ2.id)
        self.alarmDAO.insertAlarm(alarm)

    def checkForUnknownPosAfterZ3(self, eventZ3: EventWS, eventZ5: EventWS):
        if eventZ3 is None:
            return
        payloadZ1 = json.loads(eventZ3.payload)
        palletIdZ1 = payloadZ1["PalletID"]
        if str(palletIdZ1) != "-1":
            return
        serverTime = datetime.datetime.now()
        if eventZ3 is not None:
            timediff = int((serverTime - eventZ3.serverTime).total_seconds())
            if eventZ3.serverTime < eventZ5.serverTime or timediff < 20:
                return

        if self.alarmDAO.testAlarmExist(Alarms.UNKNOWN_POS_AFTER_Z3, eventZ3.id):
            return
        description = "The moving from Zone 3 to Zone 5 has not been finished yet. (started at: " + str(
            eventZ3.serverTime) + ")"
        alarm = Alarm(Alarms.UNKNOWN_POS_AFTER_Z1.name, description, serverTime, eventZ3.id)
        self.alarmDAO.insertAlarm(alarm)

    def checkForUnkownPosAfterZ4(self, eventZ4: EventWS, eventZ5: EventWS):
        if eventZ4 is None:
            return
        payloadZ1 = json.loads(eventZ4.payload)
        palletIdZ1 = payloadZ1["PalletID"]
        if str(palletIdZ1) != "-1":
            return
        serverTime = datetime.datetime.now()
        if eventZ5 is not None:
            timediff = int((serverTime - eventZ4.serverTime).total_seconds())
            if eventZ4.serverTime < eventZ5.serverTime or timediff < 20:
                return

        if self.alarmDAO.testAlarmExist(Alarms.UNKNOWN_POS_AFTER_Z4, eventZ4.id):
            return
        description = "The moving from Zone 4 to Zone 5 has not been finished yet. (started at: " + str(
            eventZ4.serverTime) + ")"
        alarm = Alarm(Alarms.UNKNOWN_POS_AFTER_Z1.name, description, serverTime, eventZ4.id)
        self.alarmDAO.insertAlarm(alarm)

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

    def getEventsNewerThen(self, timestamp):
        dt_object = datetime.datetime.fromtimestamp((timestamp / 1000) - 3600)
        logging.debug(dt_object)
        events = self.eventsDAO.getEventByTimestamp(dt_object)
        for e in events:
            e["serverTime"] = str(
                e["serverTime"])  # FIXME vielleicht sollte man einfach ein richtiges Framework verwenden
        return events

    def insert_event(self, eventDic):
        self.eventsDAO.insert_event(eventDic)
