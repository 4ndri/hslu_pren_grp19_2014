__author__ = 'endru'
import Dev.Treiber.Ausrichtung.config as CFG
import Dev.Hardware.Stepper.Stepper as Stp


class Ausrichtung:
    def __init__(self):
        self.config = CFG.ARConfig()
        self.stepper = Stp.Stepper(self.config.dir_pin, self.config.pulse_pin, self.config.min_delay,
                                   self.config.max_delay, self.config.acc)
        print "Ausrichtung inited"

    def moveXAngle(self, angle):
        steps = abs(int(angle * self.config.angle2Step))
        steps = min(self.config.max_steps,steps)
        if angle < 0:
            self.stepper.steps_left(steps)
        else:
            self.stepper.steps_right(steps)

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        self.config.save_config()
        self.stepper = None
        self.stepper = Stp.Stepper(self.config.dir_pin, self.config.pulse_pin, self.config.min_delay,
                                   self.config.max_delay, self.config.acc)

