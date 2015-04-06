__author__ = 'endru'

import time
import Dev.Hardware.PWM.PWM_Kernel_Driver as PWMDriver

class ContinuousServo:
    def __init__(self, servo_max=180, freq=50):
        self.pwm = PWMDriver.PWM()
        self.servo_max=servo_max
        self.freq =freq
        self.angle = self.servo_max/2
        self.set_pwm()

    def set_pwm(self):
        self.pwm.servo_max(self.servo_max)
        self.pwm.set_delayed(0)
        self.pwm.pulse_length(self.angle)
        self.pwm.activate()

    def turn(self, pulse, turningTime):
        self.angle=pulse
        self.pwm.pulse_length(self.angle)
        print "Servo turn to " + str(self.angle)
        time.sleep(turningTime)
        self.angle = self.servo_max/2
        self.pwm.pulse_length(self.angle)
        print "Servo turn to " + str(self.angle)

    def turnRight(self, turningTime):
        self.turn(0,turningTime)

    def turnLeft(self, turningTime):
        self.turn(self.servo_max,turningTime)
