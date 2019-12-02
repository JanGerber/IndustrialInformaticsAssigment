import datetime
import unittest

from industrial_informatic_assigment.enum.alarms import Alarms
from industrial_informatic_assigment.monitoring.alarm import Alarm
from industrial_informatic_assigment.monitoring.monitoring_alarm_dao import MonitoringAlarmDAO
from industrial_informatic_assigment.monitoring.monitoring_event_dao import MonitoringEventDAO


class AlarmDAOTestCase(unittest.TestCase):
    def testInsertAlarm(self):
        serverTime = datetime.datetime.now()
        alarmDAO = MonitoringAlarmDAO(True)
        alarm = Alarm(Alarms.PEN_CHANGE_NOT_ENDED.name, "Short description", serverTime, "1")
        alarmDAO.insertAlarm(alarm)

        alarms = alarmDAO.getAllAlarms()
        self.assertGreater(len(alarms), 0)



if __name__ == '__main__':
    unittest.main()
