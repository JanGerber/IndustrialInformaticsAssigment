import logging

from industrial_inf_assigment.enum.phone_color import PhoneColor
from industrial_inf_assigment.enum.phone_shape import PhoneShape


class Phone:
    def __init__(self, frameShape: PhoneShape, keyboardShape: PhoneShape, screenShape: PhoneShape, color: PhoneColor):
        self.frameShape = frameShape
        self.keyboardShape = keyboardShape
        self.screenShape = screenShape
        self.color = color

    def printPhone(self):
        logging.debug("Phone: Frame: " + str(self.frameShape.value) + " Keyboard: " + str(
            self.keyboardShape.value) + " Screen: " + str(self.screenShape.value) + " Color:" + str(self.color.name))
