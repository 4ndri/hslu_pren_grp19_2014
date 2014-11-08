__author__ = 'endru'
import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import sys
import picamera
import picamera.array
import time
import io

def preview():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(5)
        camera.stop_preview()
def show_image(self):
    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
    # Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    cv2.imshow('picam img',image)

def play_video2():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        with picamera.array.PiRGBArray(camera) as stream:
            while True:
                t = clock()
                print "capture"
                camera.capture(stream, format="bgr")
                print "get img"
                img = stream.array
                print "got img"
                dt = clock() - t
                # draw_str(img, (20, 20), 'time: %.1f ms' % (dt*1000))
                cv2.imshow('picam img', img)

                if 0xFF & cv2.waitKey(5) == 27:
                    break

preview()