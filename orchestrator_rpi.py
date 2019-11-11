import uuid


class Orchestrator:

    def __init__(self):
        self.orchestratorID = uuid.uuid4()
        print("New orchestrator initiated (" + str(self.orchestratorID) + ")")
