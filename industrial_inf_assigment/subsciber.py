import logging

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
        if r.status_code == 200:
            logging.debug("Subscriber: subscribe to Zone " + str(zone.value) + "successful")
        else:
            logging.error(
                "Subscriber: subscribe to Zone " + str(zone.value) + ", IP: " + hostIP + " Status Code: " + str(
                    r.status_code))

    def subscribeToPenChangeStart(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/PenChangeStarted/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        if r.status_code == 200:
            logging.debug("Subscriber: subscribe to  pen change start successful")
        else:
            logging.error(
                "Subscriber: subscribe to pen change start failed, IP: " + hostIP + " Status Code: " + str(
                    r.status_code))

    def subscribeToPenChangeEnd(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/PenChangeEnded/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        if r.status_code == 200:
            logging.debug("Subscriber: subscribe to  pen change end successful")
        else:
            logging.error(
                "Subscriber: subscribe to pen change end failed, IP: " + hostIP + " Status Code: " + str(
                    r.status_code))

    def subscribeToDrawingStart(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/DrawStartExecution/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        if r.status_code == 200:
            logging.debug("Subscriber: subscribe to drawing start successful")
        else:
            logging.error(
                "Subscriber: subscribe to drawing start failed, IP: " + hostIP + " Status Code: " + str(
                    r.status_code))

    def subscribeToDrawingEnd(self, hostIP, endpoint):
        url = hostIP + self.port + self.baseService + "/DrawEndExecution/notifs"
        destUrl = self.ownAdress + endpoint
        r = requests.post(url, json={"destUrl": destUrl})
        if r.status_code == 200:
            logging.debug("Subscriber: subscribe to drawing end successful")
        else:
            logging.error(
                "Subscriber: subscribe to drawing failed IP: " + hostIP + " Status Code: " + str(
                    r.status_code))

    def subscribeToAllEventsOfWS(self, ws: Workstation):
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/rest/events/ws/" + str(ws.getUUID()) + "/PenChangeEnd/info")
        self.subscribeToPenChangeStart(ws.baseIp + ".1",
                                       "/rest/events/ws/" + str(ws.getUUID()) + "/PenChangeStart/info")
        self.subscribeToDrawingStart(ws.baseIp + ".1",
                                     "/rest/events/ws/" + str(ws.getUUID()) + "/DrawStartExecution/info")
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest/events/ws/" + str(ws.getUUID()) + "/DrawEndExecution/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z1_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z2_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z3_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z4_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z5_Changed/info")

    def subscribeToAllEventsOfWsSimple(self, ws: Workstation):
        endpointName = "/event"
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToPenChangeStart(ws.baseIp + ".1", "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToDrawingStart(ws.baseIp + ".1", "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1, "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2, "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3, "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4, "/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5, "/" + str(ws.getUUID()) + endpointName)
