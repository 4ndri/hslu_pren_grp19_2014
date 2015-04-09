__author__ = 'endru'
import time
import Dev.Hardware.PWM.PWM_Servo_Driver as PWMDriver


class DCController:
    def __init__(self, channel=0, servo_min=0, pulse_length=0.5, freq=1000):
        self.pwm = PWMDriver.PWM.get_pwm()
        self.channel = channel
        self.pulse_length = int(4096 * pulse_length)
        self.freq = freq

    def turn(self):
        self.pwm.setPWMFreq(self.freq)
        self.pwm.setPWM(self.channel, 0, self.pulse_length)
        print "DC on Channel " + str(self.channel) + " was set to " + str(self.pulse_length)

    def stop(self):
        self.pwm.setPWM(self.channel, 0, 0)