__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os

class ARConfig:
    def __init__(self):
        self.dirPath=os.path.dirname(os.path.abspath(__file__))
        self.file_name="ausrichtung.ini"
        self.config = CF.ConfigHandler(self.dirPath +"/"+ self.file_name)
        self.angle2Step = self.config.get_float("Ausrichtung", "angle2Step", 4.0)
        self.dir_pin = self.config.get_number("Ausrichtung", "dir_pin", 4)
        self.pulse_pin =self.config.get_number("Ausrichtung", "pulse_pin", 17)
        self.min_delay =self.config.get_number("Ausrichtung", "min_delay", 100)
        self.max_delay =self.config.get_number("Ausrichtung", "max_delay", 5000)
        self.acc =self.config.get_number("Ausrichtung", "acc", 100)

    def get_angle2Step(self):
        return self.angle2Step

    def set_angle2Step(self, angle2Step):
        self.config.set_float("Ausrichtung", "angle2Step", angle2Step)
        self.angle2Step=angle2Step

    def save_config(self):
        self.config.set_float("Ausrichtung", "angle2Step", self.angle2Step)
        self.config.set_number("Ausrichtung", "dir_pin", self.dir_pin)
        self.config.set_number("Ausrichtung", "pulse_pin", self.pulse_pin)
        self.config.set_number("Ausrichtung", "min_delay", self.min_delay)
        self.config.set_number("Ausrichtung", "max_delay", self.max_delay)
