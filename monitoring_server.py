import datetime
import json
import logging
import threading

from flask import Flask, render_template
from flask import request

from monitoring.monitoring_data import MonitoringEventDAO
from workstation.subsciber import Subscriber
from workstation.workstation import Workstation

# Logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Workstation
w2BaseUrl = "http://192.168.10"
ws = Workstation(w2BaseUrl, None)

# Subscriber
locPort = 5000
serverAddress = "http://192.168.103.202:" + str(locPort)
subscriber = Subscriber(serverAddress)
subscriber.subscribeToAllEventsOfWsSimple(ws)

# DB
eventDAO = MonitoringEventDAO(False)


app = Flask(__name__)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)

# Events API

# Add event
@app.route('/rest/ws/<string:wsId>/event', methods=['POST'])
def index(wsId):
    eventDesc = request.json

    serverTime = datetime.datetime.now()
    eventDic = {"eventID": eventDesc['id'], "ws": wsId, "senderID": eventDesc['senderID'],
                "payload": eventDesc['payload'], "serverTime": serverTime}
    eventDAO.insert_event(eventDic)

    resp = json.dumps({'thank': 'yes'}), 200, {'ContentType': 'application/json'}
    return resp


@app.route('/rest/events', methods=['GET'])
def getEvents():
    # logging.debug("Retrieving all the events...")
    allEvents = eventDAO.get_all_events()
    allEventsJson = json.dumps(allEvents)
    return allEventsJson


@app.route('/conveyor/state', methods=['GET'])
def getState():
    logging.debug("Retrieving the conveyor state...")
    now = datetime.datetime.now()
    time = now.isoformat()
    cnvMsg = {'conveyorID': 5, 'state': "working", "serverTime": time}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str

    logging.debug("Saving the conveyor state...")
    content = request.json
    logging.debug(content)
    newState = content["state"]
    logging.debug(newState)
    now = datetime.datetime.now()
    time = now.isoformat()
    cnvMsg = {'conveyorID': 5, 'state': newState, "serverTime": time}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


def detect_time_elapsed_alarms():
    pass
    # logging.debug("Checking for time elapsed alarms...")
    # sqlSt="SELECT * FROM event WHERE 1"
    # c.execute(sqlSt)
    # allRobots=c.fetchall()
    # logging.info(allRobots)


# Find alarms
def checkTimeElapsedAlarms():
    #logging.debug("Checking DB for alarms")
    detect_time_elapsed_alarms()
    threading.Timer(5.0, checkTimeElapsedAlarms).start()


if __name__ == '__main__':
    checkTimeElapsedAlarms()

    app.run("0.0.0.0", locPort)
