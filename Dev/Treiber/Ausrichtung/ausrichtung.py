__author__ = 'endru'
import Dev.Treiber.Ausrichtung.config as CFG
import Dev.Hardware.Stepper.Stepper as Stp


class Ausrichtung:
    def __init__(self):
        self.config = CFG.ARConfig()
        self.stepper = Stp.Stepper(self.config.dir_pin, self.config.pulse_pin, self.config.min_delay,
                                   self.config.max_delay, self.config.acc)
        self.curr_pos = 0
        print "Ausrichtung inited"

    def moveXAngle(self, angle):
        steps = abs(int(angle * self.config.angle2Step))
        if angle < 0:
            steps = -steps
        self.move_steps(steps)

    def move_steps(self, steps):
        #self.stepper.move_steps(steps)
        if steps < 0:
            steps = abs(steps)
            steps = max(min(self.config.max_steps + self.curr_pos, steps), 0)
            self.stepper.steps_left(steps)
            self.curr_pos = self.curr_pos - steps
        else:
            steps = max(min(self.config.max_steps - self.curr_pos, steps), 0)
            self.stepper.steps_right(steps)
            self.curr_pos = self.curr_pos + steps

    def reset(self):
        self.move_steps(-self.curr_pos)

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        self.config.save_config()
        self.stepper = None
        self.stepper = Stp.Stepper(self.config.dir_pin, self.config.pulse_pin, self.config.min_delay,
                                   self.config.max_delay, self.config.acc)

