from Dev.Test import camera

__author__ = 'endru'

import numpy as np
import cv2
import cv2.cv as cv
from Dev.Test.video import create_capture
from Dev.Test.common import clock, draw_str
from Dev.Test.BasicFunctions import *
import sys



class Annotation:
    def __init__(self, annotation_path, video_src=0):
        self.annotation_path=annotation_path
        self.video_src = video_src
        self.cam = camera.get_camera()
        self.cascade = None
        self.img = None

    def define_object(self):
        cv2.namedWindow('real image')
        cv.SetMouseCallback('real image', self.on_mouse, 0)

        pass

    def on_mouse(self, event, x, y, flags, params):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            print 'Start Mouse Position: '+str(x)+', '+str(y)
            sbox = [x, y]
            boxes.append(sbox)
        elif event == cv.CV_EVENT_LBUTTONUP:
            print 'End Mouse Position: '+str(x)+', '+str(y)
            ebox = [x, y]
            boxes.append(ebox)

    def play(self):
        try:
            errorcounter = 0
            while errorcounter<100:
                t = clock()
                ret, img = self.cam.take_picture
                if img is None:
                    errorcounter += 1
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                rects = []
                if self.cascade is not None:
                    rects = detect(gray, self.cascade)
                vis = img.copy()
                draw_rects(vis, rects, (0, 255, 0))
                if len(rects) == 0:
                    found=False

                dt = clock() - t
                draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
                display(vis)
                k = 0xFF & cv2.waitKey(5)
                if k == 32:
                    print 'space'
                    self.img = img
                    self.define_object()
                if k == 27:
                    print 'escape'
                    break
            cv2.destroyAllWindows()

        except Exception as inst:
            print type(inst)
            print inst
            self.cam.release()
            cv2.destroyAllWindows()


ann = Annotation("", 0)
ann.play()