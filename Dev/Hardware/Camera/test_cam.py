__author__ = 'endru'

import camera
import time

t = time.time()
cam = camera.ThreadPiCam()
cam.start()

img = cam.take_picture
dt = time.time() - t
t = time.time()
print "time: " + str(dt * 1000)
img2 = cam.take_picture
dt = time.time() - t
print "time: " + str(dt * 1000)
cam.close()

cam = None
