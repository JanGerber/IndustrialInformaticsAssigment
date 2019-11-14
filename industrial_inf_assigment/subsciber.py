import requests

from industrial_inf_assigment.workstation import Workstation
from industrial_inf_assigment.zone import Zone


class Subscriber:
    def __init__(self, ownAdress):
        self.ownAdress = ownAdress
        self.baseService = "/rest/events"
        self.port = ""

    def subscribeToZoneChange(self, hostIP, zone: Zone, endpoint):
        url = hostIP + self.port + self.baseService + "/Z" + str(zone.value) + "_Changed/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        print(r.status_code)

    def subscribeToPenChangeStart(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/PenChangeStarted/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        print(r.status_code)
        print("Subscribed to PenChangeStart")

    def subscribeToPenChangeEnd(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/PenChangeEnded/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        print(r.status_code)
        print("Subscribed to PenChangeEnd")

    def subscribeToDrawingStart(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/DrawStartExecution/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        print(r.status_code)
        print("Subscribed to Drawing Start")

    def subscribeToDrawingEnd(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/DrawEndExecution/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        print(r.status_code)
        print("Subscribed to Drawing End")

    def subscribeToAllEventsOfWS(self, ws: Workstation):
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/rest/events/ws/" + ws.getUUID() + "/PenChangeEnd/info")
        self.subscribeToPenChangeStart(ws.baseIp + ".1", "/rest/events/ws/" + ws.getUUID() + "/PenChangeStart/info")
        self.subscribeToDrawingStart(ws.baseIp + ".1", "/rest/events/ws/" + ws.getUUID() + "/DrawStartExecution/info")
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest/events/ws/" + ws.getUUID() + "/DrawEndExecution/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1.value,
                                   "/rest/events/ws/" + ws.getUUID() + "/Z" + Zone.Z1.value + "_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2.value,
                                   "/rest/events/ws/" + ws.getUUID() + "/Z" + Zone.Z2.value + "_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3.value,
                                   "/rest/events/ws/" + ws.getUUID() + "/Z" + Zone.Z3.value + "_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4.value,
                                   "/rest/events/ws/" + ws.getUUID() + "/Z" + Zone.Z4.value + "_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5.value,
                                   "/rest/events/ws/" + ws.getUUID() + "/Z" + Zone.Z5.value + "_Changed/info")
