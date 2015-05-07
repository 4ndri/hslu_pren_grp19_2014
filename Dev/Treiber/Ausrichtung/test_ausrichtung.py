__author__ = 'endru'
import Dev.Treiber.Zielerfassung.zielerfassung as ZF
import Dev.Treiber.Ausrichtung.ausrichtung as AR
import time

zielerfassung = ZF.Zielerfassung()
ausrichtung = AR.Ausrichtung()
while True:
    time.sleep(2)
    print "detect"
    angle = zielerfassung.detect
    ausrichtung.moveXAngle(angle)
    ch=raw_input()
    if ch=="s":
        break
