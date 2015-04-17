__author__ = 'endru'

import time
import pigpio


class Stepper:
    def __init__(self, dir_pin, pulse_pin, min_delay=100, max_delay=5000, acc=100):
        self.dir_pin = dir_pin
        self.pulse_pin = pulse_pin
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.acc = acc
        self.pi = pigpio.pi()


    def init_pigpio_pins(self):
        self.pi.wave_tx_stop()
        self.pi.wave_clear()
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        self.pi.write(self.pulse_pin, 0)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 0)

    def __del__(self):
        print "del stepper"
        self.pi.wave_tx_stop()
        self.pi.wave_clear()
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        self.pi.write(self.pulse_pin, 0)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 0)
        self.pi.stop()

    def steps_right(self, steps):
        print "steps right: " + str(steps)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 1)
        self.run_steps(steps)

    def steps_left(self, steps):
        print "steps left: " + str(steps)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 0)
        self.run_steps(steps)

    def run_steps(self, steps):
        self.pi.wave_clear()
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        wf = []

        final_delay = max(int(self.max_delay - int(float(steps) / 2) * self.acc), self.min_delay)
        print "final_delay: " + str(final_delay) + ", max_delay: " + str(self.max_delay) + ", min_delay: " + str(
            self.min_delay)
        ramp_steps = int(float(self.max_delay - final_delay) / self.acc)
        middle_steps = max(steps - 2 * ramp_steps, 0)
        # build initial ramp up
        for delay in range(self.max_delay, final_delay, -self.acc):
            wf.append(pigpio.pulse(1 << self.pulse_pin, 0, delay))
            wf.append(pigpio.pulse(0, 1 << self.pulse_pin, delay))

        # middle steps
        if middle_steps > 0:
            for delay in range(middle_steps):
                wf.append(pigpio.pulse(1 << self.pulse_pin, 0, final_delay))
                wf.append(pigpio.pulse(0, 1 << self.pulse_pin, final_delay))

        # build ramp down
        for delay in range(final_delay, self.max_delay, +self.acc):
            wf.append(pigpio.pulse(1 << self.pulse_pin, 0, delay))
            wf.append(pigpio.pulse(0, 1 << self.pulse_pin, delay))

        self.pi.wave_add_generic(wf)

        # add after existing pulses

        offset = self.pi.wave_get_micros()

        wid1 = self.pi.wave_create()

        # send ramp, stop when final rate reached

        self.pi.wave_send_once(wid1)
        print "wait offset: " + str(offset)
        time.sleep(float(offset) / 1000000.0)  # make sure it's a float

        # while self.pi.wave_tx_busy():
        # offset = self.pi.wave_get_micros()
        # time.sleep(float(offset) / 1000000.0)


