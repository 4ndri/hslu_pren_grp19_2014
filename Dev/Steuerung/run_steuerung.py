__author__ = 'endru'
import Dev.Steuerung.steuerung as ctrl
import os
import cv2
import sys
import time

t = time.time()
control = ctrl.Steuerung()
dt = time.time() - t
print "init time: " + str(dt * 1000)
cnt_info=control.get_zielerfassung.get_image
cnt_info=control.get_zielerfassung.get_image
cnt_info=control.get_zielerfassung.get_image
cnt_info=control.get_zielerfassung.get_image
cnt_info=control.get_zielerfassung.get_image
dirPath=""
if len(sys.argv)>1:
    dirPath=sys.argv[1]
else:
    dirPath = os.path.dirname(os.path.abspath(__file__))
print dirPath
cv2.imwrite(dirPath + "/static/images/image.jpg", cnt_info.img)
print "steuerung done"