import time
import explorerhat

from industrial_inf_assigment.status_code import StatusCode


class OrchestratorStatus:

    def __init__(self):
        self.status = StatusCode.IDLE
        print("New orchestrator status initiated ")

    def blink(self):
        while True:
            if self.color == StatusCode.WORKING:  # green blinking
                explorerhat.light[3].on()
                time.sleep(0.5)
                explorerhat.light[3].off()

        time.sleep(0.5)

    def changeColor(self, status: StatusCode):
        self.status = status
        if status == StatusCode.WORKING:
            explorerhat.light[1].off()
            explorerhat.light[2].off()
        elif status == StatusCode.ERROR:
            explorerhat.light[1].off()
            explorerhat.light[2].on()
            explorerhat.light[3].off()
        elif status == StatusCode.IDLE:
            explorerhat.light[1].on()
            explorerhat.light[2].off()
            explorerhat.light[3].off()
