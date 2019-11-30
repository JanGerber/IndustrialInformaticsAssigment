class EventWS:

    def __init__(self, id, eventID, ws, senderID, payload, serverTime):
        self.id = id
        self.eventID = eventID
        self.ws = ws
        self.senderID = senderID
        self.payload = payload
        self.serverTime = serverTime
