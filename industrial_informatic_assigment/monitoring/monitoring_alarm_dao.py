import logging
import sqlite3
from threading import Lock

from industrial_informatic_assigment.enum.alarms import Alarms
from industrial_informatic_assigment.monitoring.alarm import Alarm


class MonitoringAlarmDAO:

    def __init__(self, inMemory):
        if inMemory:
            self.conn = sqlite3.connect(':memory:', check_same_thread=False,
                                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        else:
            self.conn = sqlite3.connect('monitoring.db', check_same_thread=False,
                                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        self.lock = Lock()
        self.c = self.conn.cursor()
        self.lock.acquire(True)
        self.c.execute("""CREATE TABLE IF NOT EXISTS alarm (
                     id INTEGER PRIMARY KEY,
                     alarmtype text,
                     description text,
                     serverTime timestamp,
                     eventId text
                     )""")
        self.lock.release()

    def insertAlarm(self, alarm: Alarm):
        logging.debug("MonitoringAlarmDAO: inserting alarm")
        with self.conn:
            self.lock.acquire(True)
            self.c.execute("""INSERT INTO alarm VALUES (:id, :alarmType, :description, :serverTime, :eventId)""",
                           {'id': alarm.id, 'alarmType': alarm.alarmType, 'description': alarm.description,
                            'serverTime': alarm.serverTime, 'eventId': alarm.eventId})
            self.lock.release()

    def getAllAlarms(self):
        self.lock.acquire(True)
        self.c.execute("""SELECT * FROM alarm WHERE 1""")
        alarms = self.c.fetchall()
        self.lock.release()
        return alarms

    def getAllNewAlarms(self, currentId):
        self.lock.acquire(True)
        self.c.execute("""SELECT * FROM alarm WHERE alarm.id > :currentId""", {"currentId": currentId})
        alarms = self.c.fetchall()
        self.lock.release()
        return alarms

    def testAlarmExist(self, alarmType: Alarms, eventId):
        self.lock.acquire(True)
        self.c.execute("""SELECT * FROM alarm WHERE alarm.alarmtype LIKE :alarmType AND alarm.eventId LIKE :eventId""",
                       {"alarmType": alarmType.name, "eventId": eventId})
        alarms = self.c.fetchall()
        self.lock.release()
        if len(alarms) > 0:
            return True
        return False
