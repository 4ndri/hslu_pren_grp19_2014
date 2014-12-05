__author__ = 'endru'
#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
import camera
from common import clock, draw_str

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt
    print help_message
    # args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    cam = camera.get_camera()
    # cascade_fn = args.get('--cascade', "../cascades/lbpcascades/lbpcascade_frontalface.xml")
    # cascade_fn = args.get('--cascade', "../cascades/trashcan_classifier.xml")

    cascade = cv2.CascadeClassifier("../cascades/trashcan_classifier.xml")


    while True:
        img = cam.take_picture
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()