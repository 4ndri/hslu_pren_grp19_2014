__author__ = 'endru'

import camera

cam = camera.ThreadPiCam()
cam.start()

img = cam.take_picture


cam.stop()
cam = None