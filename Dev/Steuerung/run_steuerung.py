__author__ = 'endru'
import Dev.Steuerung.steuerung as ctrl
import os
import cv2
import sys
import time


t = time.time()
control = ctrl.Steuerung()

def get_img():
    t=time.time()
    ret=control.get_zielerfassung.get_image()
    print "img1 time: " + str((time.time() - t) * 1000)
    return ret

dt = time.time() - t
print "init time: " + str(dt * 1000)


img=get_img()
img=get_img()
img=get_img()
img=get_img()
img=get_img()
dirPath=""
if len(sys.argv)>1:
    dirPath=sys.argv[1]
else:
    dirPath = os.path.dirname(os.path.abspath(__file__))
print dirPath
cv2.imwrite(dirPath + "/static/images/image.jpg", img)
print "steuerung done"



