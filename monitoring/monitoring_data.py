import logging
import sqlite3

from enum.event import Event


class MonitoringEventDAO:

    def __init__(self, inMemory):
        if inMemory:
            self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        else:
            self.conn = sqlite3.connect('monitoring.db', check_same_thread=False)

        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS event (
                     id INTEGER PRIMARY KEY,
                     eventID text,
                     ws text,
                     senderID text,
                     payload text,
                     serverTime timestamp
                     )""")

    # DB operations
    def insert_event(self, event):
        logging.debug("Inserting event:")
        logging.debug(event)
        with self.conn:
            self.c.execute("""INSERT INTO event VALUES (NULL, :eventID, :ws, :senderID, :payload, :serverTime)""",
                           {'eventID': event["eventID"], 'ws': event["ws"], 'senderID': event['senderID'],
                            'payload': event["payload"], 'serverTime': event["serverTime"]})

    def display_all_events(self):
        logging.debug("Displaying all events in the DB...")
        allEvents = self.get_all_events()
        logging.debug(allEvents)

    def get_all_events(self):
        self.c.execute("""SELECT * FROM event WHERE 1""")
        events = self.c.fetchall()
        return events

    def getLastEvent(self, event: Event):
        pass
