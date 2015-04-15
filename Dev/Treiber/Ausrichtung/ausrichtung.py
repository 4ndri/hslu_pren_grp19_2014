__author__ = 'endru'
import Dev.Treiber.Ausrichtung.config as CFG
import Dev.Hardware.Stepper.Stepper as Stp

class Ausrichtung:
    def __init__(self):
        self.config=CFG.ARConfig()
        self.stepper=Stp.Stepper(self.config.dir_pin,self.config.pulse_pin,self.config.min_delay)

    def moveXAngle(self, angle):
        steps=angle*self.config.angle2Step
        self.stepper.moveSteps(steps)

    @property
    def get_config(self):
        return self.config



