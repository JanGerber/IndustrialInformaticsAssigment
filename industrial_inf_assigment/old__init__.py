import time
import explorerhat

from industrial_inf_assigment.button_input import ButtonInput
from industrial_inf_assigment.orchestrator_rpi import Orchestrator

orchestrator = Orchestrator()

buttonInput = ButtonInput(orchestrator)

explorerhat.touch.pressed(buttonInput.changeState)

while True:
    time.sleep(1)

explorerhat.pause()
