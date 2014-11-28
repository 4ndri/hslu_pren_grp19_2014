import math

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
        self.approx_ratio = calc_ratio_compare(self.approx_rect.width, self.approx_rect.height)
        self.field_area = 0
        self.max_area_diff = 0
        self.max_width_diff = 0
        self.max_height_diff = 0
        self.max_ratio_diff = 0
        self.max_center_diff = 480
        self.image_center = Point(0, 0)
        self.set_approx_rect(approx_rect)

    def set_field(self, field=Field(0, 0, 640, 480)):
        self.field = field
        self.set_approx_rect(self.approx_rect)

    def calc_values(self):
        self.approx_area = self.approx_rect.width * self.approx_rect.height
        self.field_area = self.field.width * self.field.height
        self.max_area_diff = max(calc_area_diff(self.field_area, self.approx_area), calc_area_diff(self.approx_area, 0))
        self.max_width_diff = max(self.field.width - self.approx_rect.width, self.approx_rect.width)
        self.max_height_diff = max(self.field.height - self.approx_rect.height, self.approx_rect.height)
        self.max_ratio_diff = max(calc_ratio_compare(self.field.width, 1), calc_ratio_compare(1, self.field.height))
        self.image_center = Point(self.field.width/2, self.field.height/2)
        self.max_center_diff = self.image_center

    def set_approx_rect(self, approx_rect=Rect(100, 100)):
        approx_rect.height = min(approx_rect.height, self.field.height)
        approx_rect.width = min(approx_rect.width, self.field.width)
        self.approx_rect = approx_rect
        self.calc_values()

    def magic_sort(self, cnt):
        x, y, w, h = cv2.boundingRect(cnt)

        tmp_area = cv2.contourArea(cnt)
        area_diff = calc_area_diff(self.approx_area, tmp_area)
        p_area = float(area_diff) / self.max_area_diff

        width_diff = abs(self.approx_width - w)
        p_width = float(width_diff) / self.max_width_diff

        height_diff = abs(self.approx_height-h)
        p_height = float(height_diff) / self.max_height_diff

        tmp_ratio = calc_ratio_compare(w, h)
        ratio_diff = abs(tmp_ratio - self.approx_ratio)
        p_ratio = float(ratio_diff) / self.max_ratio_diff

        m = Point(x + w/2, y + h/2)

        center_distance = Point(abs(self.image_center.x - m.x), abs(self.image_center.y - m.y))
        center_diff = center_distance.distance(Point(0, 0))
        p_center = float(center_diff)/self.max_center_diff

        p = p_area * p_width * p_height * p_ratio * p_center
        return p

    def magic_finder(self, image, contours):

        """

        :rtype : object
        """

        cnt_sort = sorted(contours, key=self.magic_sort, reverse=False)
        cnt = cnt_sort[0]
        return cnt


def calc_ratio_compare(w, h):
    """
    :param w: int
    :param h: int
    :rtype : float
    """
    r = float(w) / h
    if r < 1:
        r = 2 - 1 / r
    return r

def calc_area_diff(a1, a2):
    """
    :param a1: float
    :param a2: float
    :rtype : float
    """
    area_diff = abs(math.sqrt(a1)-math.sqrt(a2))
    return area_diff

class Rect:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other_point):
        """

        :param other_point: Point
        :return: float
        """
        w = self.x - other_point.x
        h =  self.y - other_point.y
        r = math.sqrt(math.pow(w, 2) + math.pow(h, 2))
        return r


class Field:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width= width
        self.height = height