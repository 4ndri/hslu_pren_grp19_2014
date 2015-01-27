import sys

__author__ = 'endru'
import math
import camera
import ContourFinder as cf
import cv2
import cv2.cv as cv
import numpy as np
import time


cam = camera.get_camera()
try:
    threshold_val = 70
    cnt_calculator = cf.ContourCalc(cf.Rect(640, 480), cf.Field(0, 0, 640, 480), cf.Rect(100,120))

    while True:

        t = time.time()
        img = cam.take_picture
        cnt_info = cnt_calculator.find_contours(img)

        k = 0xFF & cv2.waitKey(5)
        if k != 255:
            print k
        if k == 27:
            print 'escape'
            break
        if k == 114:
            cnt_calculator.field_top_up()
            print 'field top up  ' + str(cnt_calculator.field.y)
        if k == 102:
            cnt_calculator.field_top_down()
            print 'field top down ' + str(cnt_calculator.field.y)
        if k == 117:
            cnt_calculator.field_bottom_up()
            print 'field bottom up ' + str(cnt_calculator.field.y)
        if k == 106:
            cnt_calculator.field_bottom_down()
            print 'field bottom down ' + str(cnt_calculator.field.y)
        if k == 81:
            cnt_calculator.threshold_decrease()
            print 'threshold down ' + str(cnt_calculator.threshold)
        if k == 83:
            cnt_calculator.threshold_increase()
            print 'threshold up ' + str(cnt_calculator.threshold)
        dt = time.time() - t
        if cnt_info is None:
            continue

        print '%s\r' % ' '*20, # clean up row
        print 'time: %.1f ms' % (dt*1000) + '\t |\t distance: %.lf px' % cnt_info.center_distance.x + '\t |\t area: %.lf px' % cnt_info.area,
except Exception as ex:
    print "Unexpected error:", ex
finally:
    cam.close()
    cv2.destroyAllWindows()
