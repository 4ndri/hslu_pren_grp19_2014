__author__ = 'endru'
import Dev.Hardware.DCMotor.WiringPiDC as WDC
import time

dc = WDC.DCController(0.5,1000,13,0.05,0.1)

dc.run(0.5)
while True:
    time.sleep(5)
    ch=raw_input()
    if ch=="s":
        break

dc.stop()