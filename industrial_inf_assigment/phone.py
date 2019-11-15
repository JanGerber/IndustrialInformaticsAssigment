from industrial_inf_assigment.phone_color import PhoneColor
from industrial_inf_assigment.phone_shape import PhoneShape


class Phone:
    def __init__(self, frameShape: PhoneShape, keyboardShape: PhoneShape, screenShape: PhoneShape, color: PhoneColor):
        self.frameShape = frameShape
        self.keyboardShape = keyboardShape
        self.screenShape = screenShape
        self.color = color
