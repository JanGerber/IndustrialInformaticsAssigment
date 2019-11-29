from enum import Enum


class Event(Enum):
    Z1_Changed = "Z1_Changed"
    Z2_Changed = "Z2_Changed"
    Z3_Changed = "Z3_Changed"
    Z4_Changed = "Z4_Changed"
    Z5_Changed = "Z5_Changed"
    PenChangeStarted = "PenChangeStarted"
    DrawStartExecution = "DrawStartExecution"
    DrawEndExecution = "DrawEndExecution"
