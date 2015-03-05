__author__ = 'endru'

import numpy as np
import cv2
import cv2.cv as cv
from Dev.Test.video import create_capture
from Dev.Test.common import clock, draw_str


def draw_rects(img, rects, color):
    """

    :rtype : object
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def take_picture(cam):
    """

    :rtype : object
    """
    img = cam.read()
    return img

def display(img, title='Image'):
    """

    :type img: object
    """
    cv2.imshow(title, img)
