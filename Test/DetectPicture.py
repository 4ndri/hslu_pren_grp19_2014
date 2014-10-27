__author__ = 'endru'


import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import sys




class TargetCalculator:
    def __init__(self, cascade_path, video_src=0, do_display=True, pos_tolerance=20):
        """

        :type video_src: int
        :type cascade_path: str
        :type do_display: bool
        :type pos_tolerance: int
        """
        self.cascade_path=cascade_path
        self.cascade = cv2.CascadeClassifier(cascade_path)
        self.do_display=do_display
        self.video_src=video_src
        self.cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
        self.pos_tolerance = pos_tolerance

    def take_picture(self):
        """

        :rtype : object
        """
        img = self.cam.read()
        return img

    @property
    def calculate_target(self):
        y = 0
        x = 0
        counter = 0
        last_pos=Point(sys.maxint,sys.maxint)
        while counter < 3:
            
            ret, img = self.take_picture()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
    
            t = clock()
            rects = detect(gray, self.cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))
            
            if len(rects) == 0:
                rect=rects[0]
                x = (rect.x1+rect.x2)/2
                y = (rect.y1+rect.y2)/2
    
            position = Point(x,y)
            if self.are_near(position,last_pos):
                counter+=1
            else:
                counter=0
            last_pos = position
            dt = clock() - t
            draw_str(vis, (20, 20), 'position: %.1f ms' % (dt*1000))
            self.display(vis)
        print('x: ', x, ' | y: ', y)
        return x

    def are_near(self, a, b):
        """

        :rtype : bool
        :param a: Point
        :param b: Point
        """
        if abs(a.x-b.x) < self.pos_tolerance and abs(a.y-b.y) < self.pos_tolerance:
            return True
        return False


        

    def display(self, img):
        """

        :type img: object
        """
        if self.do_display:
            cv2.imshow('calc target', img)




def draw_rects(self, img, rects, color):
    """

    :rtype : object
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
def detect(self, img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

class Point:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self, x=0, y=0):
        """ Create a new point at the origin 
        :rtype : Point
        :type y: float
        :type x: float
        """
        self.x = x
        self.y = y