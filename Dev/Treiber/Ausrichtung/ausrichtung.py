__author__ = 'endru'
import Dev.Treiber.Ausrichtung.config as CFG
class Ausrichtung:
    def __init__(self):
        self.stepper=None
        self.config=CFG.ARConfig()

    def moveXAngle(self, angle):
        steps=angle*self.config.angle2Step
        self.stepper.moveSteps(steps)

    @property
    def get_config(self):
        return self.config



