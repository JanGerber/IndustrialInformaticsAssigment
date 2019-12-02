from industrial_informatic_assigment.enum.alarms import Alarms


class Alarm:
    def __init__(self, alarmType, description, serverTime, eventId):
        self.id = None
        self.alarmType = alarmType
        self.description = description
        self.serverTime = serverTime
        self.eventId = eventId
