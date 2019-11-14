import json
import threading

from flask import Flask

from industrial_inf_assigment.orchestrator_input import OrchestratorInput
from industrial_inf_assigment.orchestrator_rpi import Orchestrator
from industrial_inf_assigment.orchestrator_status import OrchestratorStatus
from industrial_inf_assigment.subsciber import Subscriber
from industrial_inf_assigment.workstation import Workstation

# Workstations
w9 = Workstation("http://192.168.2", None)

# Subscribers
sub = Subscriber("http://192.168.0.108:5000")
sub.subscribeToPenChangeEnd("http://192.168.2.1", "/rest/events/PenChangeEnd/info")
sub.subscribeToPenChangeStart("http://192.168.2.1", "/rest/events/PenChangeStart/info")
sub.subscribeToDrawingStart("http://192.168.2.1", "/rest/events/DrawStartExecution/info")
sub.subscribeToDrawingEnd("http://192.168.2.1", "/rest/events/DrawEndExecution/info")

# Orchestration
orchestratorStatus = OrchestratorStatus()
orchestrator = Orchestrator(orchestratorStatus)
orchestratorInput = OrchestratorInput(orchestrator)

app = Flask(__name__)


def runFlaskApp():
    if __name__ == '__main__':
        app.run("0.0.0.0")


threadOrchestration = threading.Thread(target=orchestrator.runOrchestation, args=())
threadOrchestrationInput = threading.Thread(target=orchestratorInput.startListening, args=())
threadOrchestrationStatus = threading.Thread(target=orchestratorStatus.blink, args=())
threadFlask = threading.Thread(target=runFlaskApp, args=())

threadOrchestration.start()
threadOrchestrationStatus.start()
threadFlask.start()
threadOrchestrationInput.start()



@app.route('/rest/events/PenChangeEnd/info', methods=['POST'])
def penSelectedEndEvent():
    orchestrator.penSelectedEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/PenChangeStart/info', methods=['POST'])
def penSelectedStartEvent():
    orchestrator.penSelectedStartEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/DrawStartExecution/info', methods=['POST'])
def drawingStartEvent():
    print("Draw Start Event")
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/DrawEndExecution/info', methods=['POST'])
def drawingEndEvent():
    print("Draw End Event")
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str
