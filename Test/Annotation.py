__author__ = 'endru'

import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
from BasicFunctions import *
import sys



class Annotation:
    def __init__(self, annotation_path, video_src=0):
        self.annotation_path=annotation_path
        self.video_src=video_src
        self.cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
        self.cascade = None


    def play(self):
        try:
            errorcounter = 0
            while errorcounter<100:
                t = clock()
                ret, img = take_picture(self.cam)
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

                if k == 27:
                    print 'escape'
                    break
            cv2.destroyAllWindows()

        except Exception as inst:
            print type(inst)
            print inst
            self.cam.release()
            cv2.destroyAllWindows()

ann = Annotation("", 1)
ann.play()