__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os

class ARConfig:
    def __init__(self):
        self.dirPath=os.path.dirname(os.path.abspath(__file__))
        self.file_name="ausrichtung.ini"
        self.config = CF.ConfigHandler(self.dirPath +"/"+ self.file_name)
        self.angle2Step = self.config.get_number("Ausrichtung", "angle2Step", 4)

    def get_angle2Step(self):
        return self.angle2Step

    def set_angle2Step(self,angle2Step):
        self.config.set_number("Ausrichtung", "angle2Step", angle2Step)
        self.angle2Step=angle2Step
