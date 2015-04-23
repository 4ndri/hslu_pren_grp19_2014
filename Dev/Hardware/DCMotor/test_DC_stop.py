__author__ = 'endru'
import Dev.Hardware.DCMotor.WiringPiDC as WDC
import wiringpi2 as wiringpi
import time

gpio_pin=13

dc = WDC.DCController(0.5,1000,13,0.05,0.1)
dc.stop()
wiringpi.pwmWrite(gpio_pin, 0)
wiringpi.pinMode(gpio_pin, 1)
wiringpi.digitalWrite(gpio_pin, 0)
time.sleep(1)
