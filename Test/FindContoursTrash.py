
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
image_center = (field_rect[2]/2, field_rect[3]/2)

def magicSort(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    tmp_ratio = float(w)/h

    area_diff = abs(approx_area - w*h)

    ratio_diff = abs(approx_ratio - tmp_ratio)

    m_x = x + w/2
    m_y = y + h/2

    # M = cv2.moments(cnt)
    # centroid_x = int(M['m10']/M['m00'])
    # centroid_y = int(M['m01']/M['m00'])

    center_distance_x = abs(image_center[0] - m_x)
    center_distance_y = abs(image_center[1] - m_y)
    center_diff = math.sqrt(center_distance_x + center_distance_y)

    p_area = float(area_diff)
    p_ratio = float(ratio_diff)
    p_center = float(center_diff)
    p = p_area + p_ratio + p_center
    return p

def magicFinder(image, contours):

    """

    :rtype : object
    """
    sorted(contours, key=magicSort)
    cnt = contours[0]
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
    ret, thresh = cv2.threshold(img_gray, 70, 255, 0)
    edges = cv2.Canny(img_gray, 100, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = magicFinder(img, contours)
    # cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)
    # cv2.rectangle(img, (field_rect[1], field_rect[1]+field_rect[3]), (field_rect[0], field_rect[0]+field_rect[2]), (0, 0, 255), 3)

    cv2.rectangle(img, (field_rect[0], field_rect[1]), (field_rect[0]+field_rect[2], field_rect[1]+field_rect[3]), (0, 200, 200), 3)

    mask = np.zeros(img_gray.shape, np.uint8)

    cv2.drawContours(mask, [cnt], 0, 255, -1)

    cv2.drawContours(img_crop, contours, -1, (100, 200, 0), 1)
    cv2.drawContours(img_crop, [cnt], -1, (0, 0, 255), 1)
    # cv2.imshow('grey', img_gray)
    cv2.imshow('threshold', thresh)
    cv2.imshow('edges', edges)
    cv2.imshow('color', img_crop)
    cv2.imshow('whole', img)
    cv2.imshow('mask', mask)

    k = 0xFF & cv2.waitKey(5)
    if k == 27:
        print 'escape'
        break
cam.close()
cv2.destroyAllWindows()