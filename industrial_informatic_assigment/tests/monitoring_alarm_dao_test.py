import datetime
import unittest

from industrial_informatic_assigment.monitoring.alarm import Alarm
from industrial_informatic_assigment.monitoring.monitoring_alarm_dao import MonitoringAlarmDAO
from industrial_informatic_assigment.monitoring.monitoring_event_dao import MonitoringEventDAO


class AlarmDAOTestCase(unittest.TestCase):
    def testInsertAlarm(self):
        serverTime = datetime.datetime.now()
        alarmDAO = MonitoringAlarmDAO(True)
        alarm = Alarm()
        alarmDAO.insert_event(eventDic)



if __name__ == '__main__':
    unittest.main()
