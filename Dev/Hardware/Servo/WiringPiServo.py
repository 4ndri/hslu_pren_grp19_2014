__author__ = 'endru'

import wiringpi2 as wiringpi
import time


class ContinuousServo:
    def __init__(self, duty_min=1.4, duty_max=1.6, gpio_pin=18):
        print "init wservo"
        self.range = 1024
        self.gpio_pin = gpio_pin
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty = 1.5
        self.clock = 1
        self.set_pwm()
        self.set_clock()


    def set_clock(self):
        self.clock = int(float(19200000) / (self.range * float(1000) / self.get_period()))
        wiringpi.pwmSetClock(self.clock)

    def get_period(self):
        """

        :rtype : float
        """
        return self.duty + 20

    def __del__(self):
        print "del wiringpi servo"
        wiringpi.pwmWrite(self.gpio_pin, 0)  # switch PWM output to 0
        wiringpi.pinMode(self.gpio_pin, 0)

    def set_pwm(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.gpio_pin, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetRange(self.range)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turn(self, duty, turningTime):
        self.duty = duty
        self.set_clock()
        range = int(float(self.range) / self.get_period() * self.duty)
        wiringpi.pwmWrite(self.gpio_pin, range)
        print "Servo turn: duty: " + str(self.duty) + "ms  period: " + str(self.get_period()) + "ms"
        time.sleep(turningTime)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turnRight(self, turningTime):
        self.turn(self.duty_min, turningTime)

    def turnLeft(self, turningTime):
        self.turn(self.duty_max, turningTime)