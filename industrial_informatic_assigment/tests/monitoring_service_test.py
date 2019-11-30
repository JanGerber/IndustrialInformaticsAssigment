import json
import unittest

from industrial_informatic_assigment.monitoring.monitoring_event_dao import MonitoringEventDAO
from industrial_informatic_assigment.monitoring.monitoring_service import MonitoringService


class MyTestCase(unittest.TestCase):
    def testGetStatusWS(self):
        eventDAO = MonitoringEventDAO(True)
        service = MonitoringService(eventDAO, None)
        status = service.getStatusOfWS()
        cnvMsg_str = json.dumps(vars(status))
        print(cnvMsg_str)


if __name__ == '__main__':
    unittest.main()
