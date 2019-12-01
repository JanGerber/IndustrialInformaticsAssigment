from enum import Enum


class ConveyorStatus(Enum):
    OCCUPIED = "Occupied"
    FREE = "Free"
    UNKNOWN = "Unknown"
