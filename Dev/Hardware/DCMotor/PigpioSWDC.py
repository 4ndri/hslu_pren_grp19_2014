__author__ = 'endru'
import pigpio
import time


class DCController:
    def __init__(self, pulse_length=0.5, freq=1000, gpio_pin=13, acc=0.05, ramp_wait=0.05):
        self.pi = pigpio.pi()
        self.gpio_pin = gpio_pin
        self.is_running = False
        self.freq = freq
        self.acc = acc
        self.ramp_wait = ramp_wait
        self.pulse_length = pulse_length
        self.current_pulse_length = 0
        self.range = 1000
        self.set_pwm()

    def __del__(self):
        print "PigpioSWDC del on gpio " + str(self.gpio_pin)
        pi = pigpio.pi()
        pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        pi.write(self.gpio_pin, 0)

    def set_pwm(self):
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        self.pi.write(self.gpio_pin, 0)
        self.pi.set_PWM_frequency(self.gpio_pin,self.freq)
        self.pi.set_PWM_range(self.gpio_pin, self.range)
        self.pi.set_PWM_dutycycle(self.gpio_pin,0)

    def run(self, pulse_length=0):
        if not self.is_running:
            self.current_pulse_length = 0
        self.is_running = True

        if pulse_length != 0:
            self.pulse_length = pulse_length

        self.ramp_dc(self.current_pulse_length, self.pulse_length)

    def set_range(self, pulse_length=0):
        if pulse_length != 0:
            self.current_pulse_length = pulse_length
        self.current_pulse_length=min(self.current_pulse_length,1)
        duty_cycle = int(float(self.range) * self.current_pulse_length)
        self.pi.set_PWM_dutycycle(self.gpio_pin,duty_cycle)
        print "PigpioSWDC on gpio " + str(self.gpio_pin) + " was set to " + str(self.current_pulse_length)

    def set_pulse_length(self, pulse_length):
        self.pulse_length = pulse_length
        if self.is_running:
            self.run()

    def ramp_dc(self, start, end):
        start=max(0,start)
        end=max(0,end)
        if start<end:
            while start < end:
                self.set_range(start)
                start = self.current_pulse_length + self.acc
                time.sleep(self.ramp_wait)
        else:
            while start > end:
                self.set_range(start)
                start = self.current_pulse_length - self.acc
                time.sleep(self.ramp_wait)
        self.set_range(end)

    def stop(self):
        print "PigpioDC stop on gpio " + str(self.gpio_pin)
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)
        self.pi.write(self.gpio_pin, 0)
        self.current_pulse_length = 0
        self.is_running = False