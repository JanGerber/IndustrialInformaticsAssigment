from enum import Enum


class RobotStatus(Enum):
    IDLE = "Idle"
    DRAWING = "Drawing"
    PEN_CHANGE = "Pen changing"
    UNKNOWN = "Unkown"
