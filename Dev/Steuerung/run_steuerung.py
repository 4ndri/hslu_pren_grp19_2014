__author__ = 'endru'
import Dev.Steuerung.steuerung as ctrl
import os
import cv2
import sys
import time


t = time.time()
control = ctrl.Steuerung()

control.start()
print "running time: " + str((time.time() - t) * 1000)
print "fertig"



