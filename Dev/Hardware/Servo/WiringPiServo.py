__author__ = 'endru'

import wiringpi2 as wiringpi
import time


class ContinuousServo:
    def __init__(self, freq=45, duty_min=1.4, duty_max=1.6, gpio_pin=18):
        print "init wservo"
        self.gpio_pin = gpio_pin
        self.freq = freq
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty = 1.5
        self.clock = int(float(19200000) / 1024 / self.freq)
        self.range = 1024
        self.set_pwm()

    def __del__(self):
        print "del wiringpi servo"
        wiringpi.pwmWrite(self.gpio_pin, 0)  # switch PWM output to 0
        wiringpi.pinMode(self.gpio_pin, 0)

    def set_pwm(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.gpio_pin, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(self.clock)
        wiringpi.pwmSetRange(self.range)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turn(self, duty, turningTime):
        self.duty = duty
        range = int(float(self.range) / (float(1000) / self.freq) * self.duty)
        # range = int(float(self.range) / self.servo_max * self.angle)
        wiringpi.pwmWrite(self.gpio_pin, range)
        print "Servo turn to " + str(self.duty)
        time.sleep(turningTime)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turnRight(self, turningTime):
        self.turn(self.duty_min, turningTime)

    def turnLeft(self, turningTime):
        self.turn(self.duty_max, turningTime)