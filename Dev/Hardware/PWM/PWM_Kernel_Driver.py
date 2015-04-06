__author__ = 'endru'
import time


class PWM:
    def __init__(self):
        self.pwm_path = "/sys/class/rpi-pwm/pwm0/"
        pass

    def set(self, prop, value):
        try:
            f = open(self.pwm_path + prop, 'w')
            f.write(value)
            f.close()
        except:
            print("Error writing to: " + prop + " value: " + value)

    def activate(self):
        self.set("active", "1")

    def deactivate(self):
        self.set("active", "0")

    def set_delayed(self, delay=0):
        if delay == 0:
            self.set("delayed", "0")
        else:
            self.set("delayed", "1")

    def servo_max(self, servo_max):
        self.set("servo_max", str(servo_max))

    def pulse_length(self, pulse_length):
        self.set("servo", str(pulse_length))

    def set_frequency(self, freq):
        self.set("frequency", str(freq))

    def set_mode(self, mode):
        self.set("mode", str(mode))