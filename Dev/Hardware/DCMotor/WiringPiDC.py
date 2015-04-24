__author__ = 'endru'
import wiringpi2 as wiringpi
import time


class DCController:
    def __init__(self, pulse_length=0.5, freq=1000, gpio_pin=13, acc=0.05, ramp_wait=0.05):
        self.gpio_pin = gpio_pin
        self.is_running = False
        self.freq = freq
        self.acc = acc
        self.ramp_wait = ramp_wait
        self.pulse_length = pulse_length
        self.current_pulse_length = 0
        self.range = 1024
        self.clock = int(float(19200000) / self.range / self.freq)
        self.set_pwm()

    def __del__(self):
        print "WiringPiDC del on gpio " + str(self.gpio_pin)
        wiringpi.pwmWrite(self.gpio_pin, 0)
        wiringpi.pinMode(self.gpio_pin, 1)
        wiringpi.digitalWrite(self.gpio_pin, 0)

    def set_pwm(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.gpio_pin, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(self.clock)
        wiringpi.pwmSetRange(self.range)
        wiringpi.pwmWrite(self.gpio_pin, 0)

    def run(self, pulse_length=0):
        if not self.is_running:
            self.current_pulse_length = 0
        self.is_running = True

        if pulse_length != 0:
            self.pulse_length = pulse_length

        self.ramp_dc(self.current_pulse_length, self.pulse_length)
        # print "WiringPiDC on gpio " + str(self.gpio_pin) + " was set to " + str(self.pulse_length)

    def set_range(self, pulse_length=0):
        if pulse_length != 0:
            self.current_pulse_length = pulse_length
        duty_cycle = int(float(self.range) * self.current_pulse_length)
        wiringpi.pwmWrite(self.gpio_pin, duty_cycle)
        print "WiringPiDC on gpio " + str(self.gpio_pin) + " was set to " + str(self.current_pulse_length)

    def set_pulse_length(self, pulse_length):
        self.pulse_length = pulse_length
        if self.is_running:
            self.run()

    def ramp_dc(self, start, end):
        while start < end:
            self.set_range(start)
            start = self.current_pulse_length + self.acc
            time.sleep(self.ramp_wait)
        self.set_range(end)

    def stop(self):
        print "WiringPiDC stop on gpio " + str(self.gpio_pin)
        wiringpi.pwmWrite(self.gpio_pin, 0)
        wiringpi.pinMode(self.gpio_pin, 1)
        wiringpi.digitalWrite(self.gpio_pin, 0)
        self.current_pulse_length = 0
        self.is_running = False