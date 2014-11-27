
__author__ = 'endru'
import math
import camera
import cv2
import cv2.cv as cv
import numpy as np

approx_height = 120
approx_width = 100
approx_area = approx_width * approx_height
approx_ratio = float(approx_width)/approx_width

field_rect = (110, 120, 300, 300)
field_area = field_rect[2] * field_rect[3]
max_area_diff = max(field_area - approx_area, approx_area)
max_width_diff = max(field_rect[2] - approx_width, approx_width)
max_height_diff = max(field_rect[3] - approx_height, approx_height)
image_center = (field_rect[2]/2, field_rect[3]/2)

def magic_sort(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    tmp_ratio = float(w)/h
    tmp_area = cv2.contourArea(cnt)
    area_diff = abs(approx_area-tmp_area)
    width_diff = abs(approx_width-w)
    height_diff = abs(approx_height-h)
    ratio_diff = abs(tmp_ratio - approx_ratio)

    m_x = x + w/2
    m_y = y + h/2

    # M = cv2.moments(cnt)
    # centroid_x = int(M['m10']/M['m00'])
    # centroid_y = int(M['m01']/M['m00'])

    center_distance_x = abs(image_center[0] - m_x)
    center_distance_y = abs(image_center[1] - m_y)
    center_diff = math.sqrt(center_distance_x + center_distance_y)

    p_area = float(area_diff) / max_area_diff
    p_width = float(width_diff) / max_width_diff
    p_height = float(height_diff) / max_height_diff
    p_ratio = float(ratio_diff)
    p_center = float(center_diff)
    p = p_area * p_width * p_height
    return p

def magic_finder(image, contours):

    """

    :rtype : object
    """
    cnt_sort = sorted(contours, key=magic_sort, reverse=False)
    cnt = cnt_sort[0]
    return cnt

def create_graph(vertex, color, new_img):
    for g in range(0, len(vertex)-1):
        for y in range(0, len(vertex[0][0])-1):
            cv2.circle(new_img, (vertex[g][0][y], vertex[g][0][y+1]), 3, (255,255,255), -1)
            cv2.line(new_img, (vertex[g][0][y], vertex[g][0][y+1]), (vertex[g+1][0][y], vertex[g+1][0][y+1]), color, 2)
    cv2.line(new_img, (vertex[len(vertex)-1][0][0], vertex[len(vertex)-1][0][1]), (vertex[0][0][0], vertex[0][0][1]), color, 2)

cam = camera.get_camera()
i = 0

while True:
    img = cam.take_picture

    img_crop = img[field_rect[1]:field_rect[1]+field_rect[3], field_rect[0]:field_rect[0]+field_rect[2]]
    img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

    #img_gray = cv2.equalizeHist(img_gray)
    ret, thresh = cv2.threshold(img_gray, 70, 255, cv2.THRESH_BINARY_INV)
    # edges = cv2.Canny(img_gray, 100, 200)
    cv2.imshow('threshold before', thresh)
    (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('threshold after', thresh)
    cnt = magic_finder(img, contours)
    # cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)
    # cv2.rectangle(img, (field_rect[1], field_rect[1]+field_rect[3]), (field_rect[0], field_rect[0]+field_rect[2]), (0, 0, 255), 3)

    cv2.rectangle(img, (field_rect[0], field_rect[1]), (field_rect[0]+field_rect[2], field_rect[1]+field_rect[3]), (0, 200, 200), 3)

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
    if k == 27:
        print 'escape'
        break
cam.close()
cv2.destroyAllWindows()