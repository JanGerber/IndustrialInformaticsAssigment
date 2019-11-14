import requests

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
