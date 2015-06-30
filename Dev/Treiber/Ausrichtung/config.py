__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os
import math

class ARConfig:
    def __init__(self):
        self.dirPath=os.path.dirname(os.path.abspath(__file__))
        self.file_name="ausrichtung.ini"
        self.config = CF.ConfigHandler(self.dirPath +"/"+ self.file_name)
        self.angle2Step = self.config.get_float("Ausrichtung", "angle2Step", 2970.8922) #float(100*float(140)/12)/math.pi*8
        self.dir_pin = self.config.get_number("Ausrichtung", "dir_pin", 10)
        self.pulse_pin =self.config.get_number("Ausrichtung", "pulse_pin", 22)
        self.enable_pin =self.config.get_number("Ausrichtung", "enable_pin", 24)
        self.microsteps1_pin =self.config.get_number("Ausrichtung", "microsteps1_pin", 9)
        self.microsteps2_pin =self.config.get_number("Ausrichtung", "microsteps2_pin", 11)
        self.min_delay =self.config.get_number("Ausrichtung", "min_delay", 300)
        self.max_delay =self.config.get_number("Ausrichtung", "max_delay", 2000)
        self.acc =self.config.get_number("Ausrichtung", "acc", 100)
        self.max_steps =self.config.get_number("Ausrichtung", "max_steps", 3200)

    def set_angle2Step(self, angle2Step):
        self.config.set_float("Ausrichtung", "angle2Step", angle2Step)
        self.angle2Step=angle2Step

    def save_config(self):
        self.config.set_float("Ausrichtung", "angle2Step", self.angle2Step)
        self.config.set_number("Ausrichtung", "dir_pin", self.dir_pin)
        self.config.set_number("Ausrichtung", "pulse_pin", self.pulse_pin)
        self.config.set_number("Ausrichtung", "enable_pin", self.enable_pin)
        self.config.set_number("Ausrichtung", "microsteps1_pin", self.microsteps1_pin)
        self.config.set_number("Ausrichtung", "microsteps2_pin", self.microsteps2_pin)
        self.config.set_number("Ausrichtung", "min_delay", self.min_delay)
        self.config.set_number("Ausrichtung", "max_delay", self.max_delay)
        self.config.set_number("Ausrichtung", "acc", self.acc)
        self.config.set_number("Ausrichtung", "max_steps", self.max_steps)
