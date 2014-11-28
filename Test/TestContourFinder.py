
__author__ = 'endru'
import math
import camera
import ContourFinder as cf
import cv2
import cv2.cv as cv
import numpy as np

cam = camera.get_camera()
threshold_val = 70
cnt_calculator = cf.ContourCalc(cf.Rect(640, 480), cf.Field(0, 0, 640, 480), cf.Rect(100,120))

while True:
    img = cam.take_picture

    img_crop = img[cnt_calculator.field.y:cnt_calculator.field.y + cnt_calculator.field.height, cnt_calculator.field.x:cnt_calculator.field.x+cnt_calculator.field.width]
    img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

    # img_gray = cv2.equalizeHist(img_gray)
    ret, thresh = cv2.threshold(img_gray, threshold_val, 255, cv2.THRESH_BINARY_INV)
    # edges = cv2.Canny(img_gray, 100, 200)
    cv2.imshow('threshold before', thresh)
    (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('threshold after', thresh)
    cnt = cnt_calculator.magic_finder(img, contours)
    # cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)
    # cv2.rectangle(img, (field_rect[1], field_rect[1]+field_rect[3]), (field_rect[0], field_rect[0]+field_rect[2]), (0, 0, 255), 3)

    cv2.rectangle(img, (cnt_calculator.field.x, cnt_calculator.field.y), (cnt_calculator.field.x + cnt_calculator.field.width, cnt_calculator.field.y + cnt_calculator.field.height), (0, 200, 200), 3)

    mask = np.zeros(img_gray.shape, np.uint8)

    cv2.drawContours(mask, [cnt], 0, 255, -1)

    cv2.drawContours(img_crop, contours, -1, (100, 200, 0), 1)
    cv2.drawContours(img_crop, [cnt], -1, (0, 0, 255), 1)
    # cv2.imshow('grey', img_gray)
    # cv2.imshow('edges', edges)
    cv2.imshow('color', img_crop)
    cv2.imshow('whole', img)
    cv2.imshow('mask', mask)

    k = 0xFF & cv2.waitKey(5)
    if k != 255:
        print k
    if k == 27:
        print 'escape'
        break
    if k == 82:
        new_field = cf.Field(cnt_calculator.field.x, cnt_calculator.field.y + 3, cnt_calculator.field.width, cnt_calculator.field.height - 3)
        cnt_calculator.set_field(new_field)
        print 'field top up  ' + str(cnt_calculator.field.y)
    if k == 84:
        new_field = cf.Field(cnt_calculator.field.x, cnt_calculator.field.y + 3, cnt_calculator.field.width, cnt_calculator.field.height - 3)
        cnt_calculator.set_field(new_field)
        print 'field top down ' + str(cnt_calculator.field.y)
    if k == 81:
        threshold_val = max(0,threshold_val - 3)
        print 'threshold down ' + str(threshold_val)
    if k == 82:
        threshold_val = min(255, threshold_val + 3)
        print 'threshold up ' + str(threshold_val)

cam.close()
cv2.destroyAllWindows()
