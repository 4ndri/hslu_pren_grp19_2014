__author__ = 'endru'

import pigpio
import time


class ContinuousServo:
    def __init__(self, duty_min=1.4, duty_max=1.6, gpio_pin=18):
        print "PigpioServo init"
        self.pi = pigpio.pi()
        self.range = 1000000
        self.gpio_pin = gpio_pin
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty = 1.5
        self.freq=0
        self.clock = 1
        self.set_pwm()
        self.set_freq()


    def set_freq(self):
        self.freq = int(float(1000)/self.get_period())

    def get_period(self):
        """

        :rtype : float
        """
        return self.duty + 20

    def __del__(self):
        print "PigpioServo del on gpio " + str(self.gpio_pin)
        pi = pigpio.pi()
        pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        pi.write(self.gpio_pin, 0)

    def set_pwm(self):
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        self.pi.write(self.gpio_pin, 0)

    def turn(self, duty, turningTime):
        self.duty = duty
        self.set_freq()
        duty_cycle = int(float(self.range) / self.get_period() * self.duty)
        self.pi.hardware_PWM(self.gpio_pin, self.freq, duty_cycle)
        print "PigpioServo turn: duty: " + str(self.duty) + "ms  period: " + str(self.get_period()) + "ms"
        time.sleep(turningTime)
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        self.pi.write(self.gpio_pin, 0)

    def turnRight(self, turningTime):
        self.turn(self.duty_min, turningTime)

    def turnLeft(self, turningTime):
        self.turn(self.duty_max, turningTime)