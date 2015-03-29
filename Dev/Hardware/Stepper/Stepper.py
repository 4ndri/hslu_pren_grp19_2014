__author__ = 'endru'

import time
import Dev.Hardware.PWM.PWM_Servo_Driver as PWMDriver


class Stepper:
    def __init__(self, channel=1, min_freq=50, max_freq=800, freq_step=10, freq_period=0.1):
        self.pwm=PWMDriver.PWM.get_pwm()
        self.channel =channel
        self.min_freq=min_freq
        self.max_freq=max_freq
        self.freq_step=freq_step
        self.freq_period=freq_period

    def turnRight(self, steps):
        self.pwm.(self.min_freq)
        self.pwm.setPWM(self.channel, 0, self.servo_min)
        print "Servo on Channel " + str(self.channel)  + " was set to " + str(self.servo_min)
        time.sleep(turningTime)
        self.pwm.setPWM(self.channel, 0, 0)
        print "Servo on Channel " + str(self.channel)  + " was set to 0"

    def turnLeft(self, steps):
        self.pwm.setPWM(self.channel, 0, self.servo_max)
        print "Servo on Channel " + str(self.channel) + " was set to " + str(self.servo_max)
        time.sleep(turningTime)
        self.pwm.setPWM(self.channel, 0, 0)
        print "Servo on Channel " + str(self.channel) + " was set to 0"