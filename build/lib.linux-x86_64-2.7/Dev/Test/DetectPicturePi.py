__author__ = 'endru'


import numpy as np
import cv2
import cv2.cv as cv
from Dev.Test.video import create_capture
from Dev.Test.common import clock, draw_str
import sys
import picamera
import picamera.array
import time
import io


class TargetCalculator:
    def __init__(self, cascade_path, do_display=True, pos_tolerance=20):
        """

        :type cascade_path: str
        :type do_display: bool
        :type pos_tolerance: int
        """

        self.cascade_path=cascade_path
        self.cascade = cv2.CascadeClassifier(cascade_path)
        self.do_display=do_display
        # self.pi_cam=None
        # self.pi_stream=None
        # print "initialize cam"
        # self.pi_cam = picamera.PiCamera()
        # self.pi_cam.start_preview()
        # time.sleep(2)
        # print "get stream"
        # self.pi_stream=picamera.array.PiRGBArray(self.pi_cam)
        # self.pi_cam.capture(self.pi_stream, format='bgr')
            # At this point the image is available as stream.array

        self.pos_tolerance = pos_tolerance

    def close(self):
        # if self.pi_cam is not None:
        #     self.pi_cam.close()
        # self.pi_cam = None
        # self.pi_stream = None
        print 'picam closed'

    def take_picture(self):
        """

        :rtype : object
        """
        print "take picture"
        img = self.pi_stream.array
        print "got img"
        cv2.imwrite('2.jpg', img)
        return img

    @property
    def calculate_target(self):
        """

        :return: object
        """
        try:
            print "calc target"
            y = 0
            x = 0
            counter = 0
            last_pos=Point(sys.maxint,sys.maxint)
            t = clock()
            dt = 0
            errorcounter = 0
            while counter < 3 and dt < 100 and errorcounter<100:
                dt = clock() - t
                ret, img = self.take_picture()

                if img is None:
                    print "no img"
                    errorcounter += 1
                    continue
                print "process img"
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)

                print "detect cascade"
                rects = detect(gray, self.cascade)
                vis = img.copy()
                draw_rects(vis, rects, (0, 255, 0))

                if len(rects) == 0:
                    continue
                rect=rects[0]
                if len(rect) != 4:
                    continue
                x = (rect[0]+rect[2])/2
                y = (rect[1]+rect[3])/2
                print 'found object at x: ', x, ' | y: ', y
                position = Point(x, y)
                if self.are_near(position,last_pos):
                    counter += 1
                else:
                    counter = 0
                last_pos = position
                draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
                draw_str(vis, (20, 40), 'position: %.1f px' % (x))
                self.display(vis)
            print 'x: ', x, ' | y: ', y
            self.close()
            return x

        except:
            self.close()
        return -sys.maxint




    def play_video(self):
        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            camera.start_preview()
            time.sleep(2)
            while True:
                t = clock()
                camera.capture(stream, format="jpeg", use_video_port=True)
                frame = np.fromstring(stream.getvalue(), dtype=np.uint8)
                stream.seek(0)
                frame = cv2.imdecode(frame, 1)
                dt = clock() - t
                draw_str(frame, (20, 20), 'time: %.1f ms' % (dt*1000))
                cv2.imshow('picam img', frame)

                if 0xFF & cv2.waitKey(5) == 27:
                    break

    def play_video2(self):
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

    @property
    def calc_target_pi(self):
        """

        :return: object
        """
        try:
            print "calc target"
            stream1 = io.BytesIO()
            with picamera.PiCamera() as camera:
                camera.start_preview()
                time.sleep(2)
                img1 = camera.capture(stream1, format='jpeg')
                cv2.imshow('calc target', img1)
                y = 0
                x = 0
                counter = 0
                last_pos=Point(sys.maxint,sys.maxint)
                t = clock()
                dt = 0
                errorcounter = 0
                with picamera.array.PiRGBArray(camera) as stream:
                    print "capture"
                    camera.capture(stream, format='bgr')
                    while counter < 3 and dt < 100 and errorcounter<100:
                        dt = clock() - t
                        print "get img"
                        ret, img = stream.array
                        print "got img"
                        if img is None:
                            print "no img"
                            errorcounter += 1
                            continue
                        print "process img"
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        gray = cv2.equalizeHist(gray)

                        print "detect cascade"
                        rects = detect(gray, self.cascade)
                        vis = img.copy()
                        draw_rects(vis, rects, (0, 255, 0))

                        if len(rects) == 0:
                            continue
                        rect=rects[0]
                        if len(rect) != 4:
                            continue
                        x = (rect[0]+rect[2])/2
                        y = (rect[1]+rect[3])/2
                        print 'found object at x: ', x, ' | y: ', y
                        position = Point(x, y)
                        if self.are_near(position,last_pos):
                            counter += 1
                        else:
                            counter = 0
                        last_pos = position
                        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
                        draw_str(vis, (20, 40), 'position: %.1f px' % (x))
                        self.display(vis)
                    print 'x: ', x, ' | y: ', y
                    self.close()
                    return x
        except:
            self.close()
            print "exception: ", sys.exc_info()[0]
        return -sys.maxint

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