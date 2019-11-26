import sqlite3


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
                     state text,
                     serverTime timestamp
                     )""")

    # DB operations
    def insert_event(self, event):
        print("Inserting event:")
        print(event)
        with self.conn:
            self.c.execute("INSERT INTO event VALUES (NULL,:eventID, :state, :serverTime)",
                           {'eventID': event["eventID"], 'state': event["state"], 'serverTime': event["serverTime"]})
        self.display_all_events()

    def display_all_events(self):
        print("Displaying all events in the DB...")
        allEvents = self.get_all_events()
        print(allEvents)

    def get_all_events(self):
        self.c.execute("SELECT * FROM event WHERE 1")
        events = self.c.fetchall()
        return events
