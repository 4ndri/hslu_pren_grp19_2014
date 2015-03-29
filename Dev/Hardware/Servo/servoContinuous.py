__author__ = 'endru'

import time
import Dev.Hardware.PWM.PWM_Servo_Driver as PWMDriver


class ContinuousServo:
    def __init__(self, channel=0, servo_min=150, servo_max=600, freq=50):
        self.pwm = PWMDriver.PWM.get_pwm()
        self.channel = channel
        self.servo_min = servo_min
        self.servo_max = servo_max
        self.freq=freq

    def turnRight(self, turningTime):
        self.pwm.setPWMFreq(self.freq)
        self.pwm.setPWM(self.channel, 0, self.servo_min)
        print "Servo on Channel " + str(self.channel) + " was set to " + str(self.servo_min)
        time.sleep(turningTime)
        self.pwm.setPWM(self.channel, 0, 0)
        print "Servo on Channel " + str(self.channel) + " was set to 0"

    def turnLeft(self, turningTime):
        self.pwm.setPWMFreq(self.freq)
        self.pwm.setPWM(self.channel, 0, self.servo_max)
        print "Servo on Channel " + str(self.channel) + " was set to " + str(self.servo_max)
        time.sleep(turningTime)
        self.pwm.setPWM(self.channel, 0, 0)
        print "Servo on Channel " + str(self.channel) + " was set to 0"