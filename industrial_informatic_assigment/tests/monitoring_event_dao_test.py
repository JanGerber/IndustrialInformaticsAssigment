import datetime
import unittest

from industrial_informatic_assigment.monitoring.monitoring_event_dao import MonitoringEventDAO


class EventDataDAOTestCase(unittest.TestCase):
    def testInsertEvent(self):
        serverTime = datetime.datetime.now()
        eventDAO = MonitoringEventDAO(True)
        eventDic = {"eventID": "123456789", "ws": "fb5a2454-2759-4f63-84bf-39eb710ffca4", "senderID": "CV2",
                    "payload": "", "serverTime": serverTime}
        eventDAO.insert_event(eventDic)


if __name__ == '__main__':
    unittest.main()
