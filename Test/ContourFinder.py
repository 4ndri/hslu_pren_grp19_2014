__author__ = 'endru'

import numpy as np
import cv2
import cv2.cv as cv


class ContourCalc:
    def __init__(self, cam_resolution=Rect(640, 480), field=Field(0, 0, 640, 480), approx_rect=Rect(100, 100)):
        self.field = field
        self.cam_resolution = cam_resolution
        self.approx_rect = approx_rect
        self.approx_area = 0
        self.field_area = 0
        self.max_area_diff = 0
        self.max_width_diff = 0
        self.max_height_diff = 0
        self.image_center = None
        self.set_approx_rect(approx_rect)

    def set_field(self, field=Field(0, 0, 640, 480)):
        self.field = field
        self.set_approx_rect(self.approx_rect)

    def calc_values(self):
        self.approx_area = self.approx_rect.width * self.approx_rect.height
        self.field_area = self.field.width * self.field.height
        self.max_area_diff = max(self.field_area - self.approx_area, self.approx_area)
        self.max_width_diff = max(self.field.width - self.approx_rect.width, self.approx_rect.width)
        self.max_height_diff = max(self.field.height - self.approx_rect.height, self.approx_rect.height)
        self.image_center = Point(self.field.width/2, self.field.height/2)

    def set_approx_rect(self, approx_rect=Rect(100, 100)):
        approx_rect.height = min(approx_rect.height, self.field.height)
        approx_rect.width = min(approx_rect.width, self.field.width)
        self.approx_rect = approx_rect
        self.calc_values()

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


class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Field:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width= width
        self.height = height