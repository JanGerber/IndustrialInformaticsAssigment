import datetime


class EventWS:

    def __init__(self, dbId, eventID, ws, senderID, payload, serverTime: datetime):
        self.id = dbId
        self.eventID = eventID
        self.ws = ws
        self.senderID = senderID
        self.payload = payload
        self.serverTime = serverTime
