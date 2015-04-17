__author__ = 'endru'
import wiringpi2 as wiringpi


class DCController:
    def __init__(self, pulse_length=0.5, freq=1000, gpio_pin=13):
        self.gpio_pin = gpio_pin
        self.freq = freq
        self.pulse_length = pulse_length
        self.current_pulse_length = 0
        self.range = 1024
        self.clock = int(float(19200000) / self.range / self.freq)
        self.set_pwm()

    def __del__(self):
        print "WiringPiDC del on gpio " + str(self.gpio_pin)
        wiringpi.pwmWrite(self.gpio_pin, 0)
        wiringpi.pinMode(self.gpio_pin, 0)

    def set_pwm(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.gpio_pin, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(self.clock)
        wiringpi.pwmSetRange(self.range)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def run(self, pulse_length=0):
        if pulse_length != 0:
            self.pulse_length = pulse_length
        duty_range = int(float(self.range) * self.pulse_length)
        wiringpi.pwmWrite(self.gpio_pin, duty_range)
        print "WiringPiDC turn to " + str(self.pulse_length)

    def set_pulse_length(self, pulse_length):
        self.pulse_length = pulse_length
        self.run()
        print "WiringPiDC on gpio " + str(self.gpio_pin) + " was set to " + str(self.pulse_length)

    def stop(self):
        print "WiringPiDC stop on gpio " + str(self.gpio_pin)
        wiringpi.pwmWrite(self.gpio_pin, 0)
        wiringpi.pinMode(self.gpio_pin, 0)