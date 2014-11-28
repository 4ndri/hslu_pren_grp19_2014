import math

__author__ = 'endru'

import numpy as np
import cv2
import cv2.cv as cv
import sys
from common import clock, draw_str

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
    area_diff = abs(math.sqrt(a1) - math.sqrt(a2))
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
        h = self.y - other_point.y
        r = math.sqrt(math.pow(w, 2) + math.pow(h, 2))
        return r


class Field:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class ContourInfo:
    def __init__(self, cnt, field):
        """

        :rtype : ContourInfo
        :param field: Point
        :type center_distance: Point
        :param cnt: object
        """
        self.field = field
        self.cnt = cnt

        x, y, w, h = cv2.boundingRect(cnt)
        self.area = cv2.contourArea(cnt)
        self.m_cnt = Point(x + w / 2, y + h / 2)
        self.m_field = Point(self.field.width / 2, self.field.height / 2)
        self.center_distance = Point(abs(self.m_cnt.x - self.m_field.x), abs(self.m_cnt.y - self.m_field.y))
        self.rect = Field(x, y, w, h)


class ContourCalc:
    def __init__(self, cam_resolution=Rect(640, 480), field=Field(0, 0, 640, 480), approx_rect=Rect(100, 100),
                 threshold=70):
        """

        :rtype : ContourCalc
        """
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
        self.threshold = threshold

    def set_threshold(self, threshold=70):
        """

        :param threshold: int
        """
        threshold = max(0, threshold)
        threshold = min(255, threshold)
        self.threshold = threshold

    def threshold_increase(self):
        self.set_threshold(self.threshold + 2)

    def threshold_decrease(self):
        self.set_threshold(self.threshold - 2)

    def set_field(self, field=Field(0, 0, 640, 480)):
        """

        :param field: Field
        """
        self.field = field
        self.field.x = min(self.cam_resolution.width, self.field.x)
        self.field.x = max(0, self.field.x)
        self.field.y = min(self.cam_resolution.height, self.field.y)
        self.field.y = max(0, self.field.y)
        self.field.width = min(self.field.width, self.cam_resolution.width - self.field.x)
        self.field.width = max(0, self.field.width)
        self.field.height = min(self.field.height, self.cam_resolution.height - self.field.y)
        self.field.height = max(0, self.field.height)
        self.set_approx_rect(self.approx_rect)

    def field_top_down(self):
        new_field = Field(self.field.x, self.field.y + 3, self.field.width, self.field.height - 3)
        self.set_field(new_field)

    def field_top_up(self):
        new_field = Field(self.field.x, self.field.y - 3, self.field.width, self.field.height + 3)
        self.set_field(new_field)

    def field_bottom_down(self):
        new_field = Field(self.field.x, self.field.y, self.field.width, self.field.height + 3)
        self.set_field(new_field)

    def field_bottom_up(self):
        new_field = Field(self.field.x, self.field.y, self.field.width, self.field.height - 3)
        self.set_field(new_field)

    def calc_values(self):
        self.approx_area = self.approx_rect.width * self.approx_rect.height
        self.field_area = self.field.width * self.field.height
        self.max_area_diff = max(calc_area_diff(self.field_area, self.approx_area), calc_area_diff(self.approx_area, 0))
        self.max_width_diff = max(self.field.width - self.approx_rect.width, self.approx_rect.width)
        self.max_height_diff = max(self.field.height - self.approx_rect.height, self.approx_rect.height)
        self.max_ratio_diff = max(calc_ratio_compare(self.field.width, 1), calc_ratio_compare(1, self.field.height))
        self.image_center = Point(self.field.width / 2, self.field.height / 2)
        self.max_center_diff = self.image_center.distance(Point(0, 0))

    def set_approx_rect(self, approx_rect=Rect(100, 100)):
        """

        :param approx_rect: Rect
        """
        approx_rect.height = min(approx_rect.height, self.field.height)
        approx_rect.width = min(approx_rect.width, self.field.width)
        self.approx_rect = approx_rect
        self.calc_values()

    def magic_sort(self, cnt):
        """

        :param cnt: Object
        :return: float
        """
        x, y, w, h = cv2.boundingRect(cnt)

        tmp_area = cv2.contourArea(cnt)
        area_diff = calc_area_diff(self.approx_area, tmp_area)
        p_area = float(area_diff) / self.max_area_diff

        width_diff = abs(self.approx_rect.width - w)
        p_width = float(width_diff) / self.max_width_diff

        height_diff = abs(self.approx_rect.height - h)
        p_height = float(height_diff) / self.max_height_diff

        tmp_ratio = calc_ratio_compare(w, h)
        ratio_diff = abs(tmp_ratio - self.approx_ratio)
        p_ratio = float(ratio_diff) / self.max_ratio_diff

        m = Point(x + w / 2, y + h / 2)

        center_distance = Point(abs(self.image_center.x - m.x), abs(self.image_center.y - m.y))
        center_diff = center_distance.distance(Point(0, 0))
        p_center = float(center_diff) / self.max_center_diff

        # p = p_area * 4 + p_width * 2 + p_height * 2 + p_ratio  + p_center * 2
        p = p_area * 5 + p_width + p_height + p_center + float(1) / max(float(1) / sys.maxint, tmp_area)
        return p

    def find_contours(self, img, do_display=True):

        """



        :param do_display: bool
        :param img: np.numpy.array
        :rtype : ContourInfo
        """
        img_crop = img[self.field.y:self.field.y + self.field.height, self.field.x:self.field.x + self.field.width]
        img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

        # img_gray = cv2.equalizeHist(img_gray)
        ret, thresh = cv2.threshold(img_gray, self.threshold, 255, cv2.THRESH_BINARY_INV)

        # th3 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # edges = cv2.Canny(img_gray, 100, 200)
        if do_display:
            cv2.imshow('threshold before', thresh)

        (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours.__len__<=0:
            return None
        cnt_sort = sorted(contours, key=self.magic_sort, reverse=False)

        cnt = cnt_sort[0]

        cnt_info = ContourInfo(cnt, self.field)
        if do_display:
            cv2.rectangle(img, (self.field.x, self.field.y),
                          (self.field.x + self.field.width, self.field.y + self.field.height), (0, 200, 200), 3)
            cv2.rectangle(img_crop, (cnt_info.rect.x, cnt_info.rect.y),
                          (cnt_info.rect.x + cnt_info.rect.width, cnt_info.rect.y + cnt_info.rect.height),
                          (255, 255, 0), 3)
            cv2.line(img_crop, (cnt_info.m_field.x, cnt_info.m_cnt.y), (cnt_info.m_cnt.x, cnt_info.m_cnt.y), (255, 0, 255), 3)

            draw_str(img, (20, 20), 'threshold: %.1f' % self.threshold)
            draw_str(img, (20, 40), 'distance x: %.1f px' % cnt_info.center_distance.x)
            draw_str(img, (20, 60), 'area: %.1f px' % cnt_info.area)

            cv2.drawContours(img_crop, contours, -1, (100, 200, 0), 1)
            cv2.drawContours(img_crop, [cnt], -1, (0, 0, 255), 3)

            # cv2.imshow('color', img_crop)
            cv2.imshow('whole', img)

            # mask = np.zeros(img_gray.shape, np.uint8)
            # cv2.drawContours(mask, [cnt], 0, 255, -1)
            # cv2.imshow('mask', mask)

        return cnt_info


