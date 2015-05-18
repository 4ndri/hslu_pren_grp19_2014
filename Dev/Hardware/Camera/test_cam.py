__author__ = 'endru'

import camera
import time

t = time.time()
cam = camera.PiCamera()
dt = time.time() - t
print 'time: %.1f ms' % (dt*1000)
while True:
    t = time.time()
    img = cam.take_picture
    print '%s\r' % ' '*20, # clean up row
    dt = time.time() - t
    print 'time: %.1f ms' % (dt*1000)
    ch=raw_input()
    if ch=="s":
        break
print "done"

