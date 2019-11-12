import threading
import time

from industrial_inf_assigment.orchestrator_status import OrchestratorStatus
from industrial_inf_assigment.status_code import StatusCode

orchStatus = OrchestratorStatus()
orchStatus.changeColor(StatusCode.IDLE)

thread_tire1 = threading.Thread(target=orchStatus.blink, args=())

thread_tire1.start

print("Now sleep")
time.sleep(5)
print("Sleep Over")

orchStatus.changeColor(StatusCode.WORKING)

print("Now sleep")
time.sleep(5)
print("Sleep Over")

orchStatus.changeColor(StatusCode.ERROR)
