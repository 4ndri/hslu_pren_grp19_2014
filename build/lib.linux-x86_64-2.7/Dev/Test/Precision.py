from Dev.Test import camera, ContourFinder

__author__ = 'endru'
import math
import Dev.Test.ContourFinder as cf
import cv2
import cv2.cv as cv
import numpy as np
import time
from Dev.Test.video import create_capture

path = '/home/endru/Documents/Development/precision_images/640_480_contours_'
threshold_val = 70
cnt_calculator = cf.ContourCalc(cf.Rect(640, 480), cf.Field(0, 0, 640, 480), cf.Rect(100,120))

cam = create_capture('synth:bg=/home/endru/Documents/Development/precision_images/640_480_pic00000.jpg', fallback='synth:bg=../cpp/lena.jpg:noise=0.05')

# img = cv2.imread("/home/endru/Documents/Development/precision_images/640_480_pic00002.jpg")
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(img_gray, 54, 255, cv2.THRESH_BINARY_INV)
# (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (100, 200, 0), 2)
# cv2.imwrite(path + '00002.jpg', img)

while True:
    img = cv2.imread("/home/endru/Documents/Development/precision_images/640_480_pic00002.jpg")
    cnt_info = cnt_calculator.find_contours(img, True)

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
    if k == 107:
        cnt_calculator.field_right_left()
        print 'field right left ' + str(cnt_calculator.field.x + cnt_calculator.field.width)
    if k == 108:
        cnt_calculator.field_right_right()
        print 'field right right ' + str(cnt_calculator.field.x + cnt_calculator.field.width)
    if k == 115:
        cnt_calculator.field_left_left()
        print 'field left left ' + str(cnt_calculator.field.x)
    if k == 100:
        cnt_calculator.field_left_right()
        print 'field left right ' + str(cnt_calculator.field.x)
    if k == 81:
        cnt_calculator.threshold_decrease()
        print 'threshold down ' + str(cnt_calculator.threshold)
    if k == 83:
        cnt_calculator.threshold_increase()
        print 'threshold up ' + str(cnt_calculator.threshold)
    if k == 32:
        print 'space'
        cv2.imwrite(path + '00002.jpg', img)
    if cnt_info is None:
        continue

    #print '%s\r' % ' '*20, # clean up row
    #print 'distance: %.lf px' % cnt_info.center_distance.x + '\t |\t area: %.lf px' % cnt_info.area,

cv2.destroyAllWindows()
