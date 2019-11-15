from enum import Enum


class PalletStatus(Enum):
    MOVING_TO_Z2 = 2
    MOVING_TO_Z3 = 3
    MOVING_TO_Z4 = 4
    MOVING_TO_Z5 = 5
    DRAWING = 6
    WAIT_PEN_CHANGE = 7
    WAITING = 8
    WAIT_FOR_REMOVAL = 8
    WAIT_FOR_MOVING = 9
