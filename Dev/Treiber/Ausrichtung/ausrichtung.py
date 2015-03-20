__author__ = 'endru'

class Ausrichtung:
    def __init__(self):
        self.stepper=None
        self.config=
        self.angle2Step=5

    def moveXAngle(self, angle):
        steps=angle*self.angle2Step
        self.stepper.moveSteps(steps)



