__author__ = 'endru'
import wiringpi2 as wiringpi
import time


class ContinuousServo:
    def __init__(self, servo_max=600,servo_min=400, freq=45, gpio_pin=18):
        self.gpio_pin = gpio_pin
        self.servo_max = servo_max
        self.servo_min=servo_min
        self.freq = freq
        self.duty_min=1.5-0.2/500*(500-self.servo_min)
        self.duty_max=1.5+0.2/500*(self.servo_max-500)
        self.duty = 1.5
        self.clock = int(float(19200000)/1024/self.freq)
        self.range = 1024
        self.set_pwm()

    def __del__(self):
        wiringpi.pwmWrite(18, 0)  # switch PWM output to 0
        wiringpi.pinMode(18, 0)

    def set_pwm(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.gpio_pin, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(self.clock)
        wiringpi.pwmSetRange(self.range)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turn(self, duty, turningTime):
        self.duty = duty
        range=int(float(self.range)/(float(1000)/self.freq)*self.duty)
        #range = int(float(self.range) / self.servo_max * self.angle)
        wiringpi.pwmWrite(self.gpio_pin, range)
        print "Servo turn to " + str(self.duty)
        time.sleep(turningTime)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def turnRight(self, turningTime):

        self.turn(self.duty_min, turningTime)

    def turnLeft(self, turningTime):
        self.turn(self.duty_max, turningTime)