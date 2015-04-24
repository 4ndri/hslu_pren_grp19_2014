__author__ = 'endru'

import os
import Dev.Config.ConfigHandler as CFG
import Dev.Treiber.Zielerfassung.ContourFinder as CF


class ZFConfig:
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "contourFinder.ini"
        self.config = CFG.ConfigHandler(self.dirPath + "/" + self.file_name)
        print self.dirPath + "/" + self.file_name
        self.resolution_w = self.config.get_number("Camera", "resolution_w", 640)
        self.resolution_h = self.config.get_number("Camera", "resolution_h", 480)
        self.field_x = self.config.get_number("Approx", "field_x", 0)
        self.field_y = self.config.get_number("Approx", "field_y", 0)
        self.field_width = self.config.get_number("Approx", "field_width", 640)
        self.field_height = self.config.get_number("Approx", "field_height", 480)
        self.approx_rect_w = self.config.get_number("Approx", "approx_rect_w", 100)
        self.approx_rect_h = self.config.get_number("Approx", "approx_rect_h", 120)
        self.threshold = self.config.get_number("Approx", "threshold", 65)
        tmp = float(150) / (450 * 205)
        self.pixelToCMFactor = self.config.get_float("ZF", "pixelToCMFactor", tmp)

    def set_resolution(self, resolution_rect):
        """

        :param resolution_rect: CF.Rect
        """
        self.resolution_h = resolution_rect.height
        self.config.set_number("Camera", "resolution_h", self.resolution_h)
        self.resolution_w = resolution_rect.width
        self.config.set_number("Camera", "resolution_w", self.resolution_w)

    def set_field(self, field):
        """

        :param field: CF.Field
        """
        self.field_x = field.x
        self.field_y = field.y
        self.field_width = field.width
        self.field_height = field.height
        self.save_field()

    def set_field_xywh(self, field_x, field_y, field_w, field_h):
        self.field_x = field_x
        self.field_y = field_y
        self.field_width = field_w
        self.field_height = field_h
        self.save_field()

    def save_field(self):
        self.config.set_number("Approx", "field_x", self.field_x)
        self.config.set_number("Approx", "field_y", self.field_y)
        self.config.set_number("Approx", "field_width", self.field_width)
        self.config.set_number("Approx", "field_height", self.field_height)

    def set_approx_rect(self, approx_rect):
        """

        :param approx_rect: CF.Rect
        """
        self.approx_rect_h = approx_rect.height
        self.approx_rect_w = approx_rect.width
        self.save_approx_rect()

    def set_approx_rect_wh(self, approx_rect_w, approx_rect_h):
        self.approx_rect_h = approx_rect_h
        self.approx_rect_w = approx_rect_w
        self.save_approx_rect()

    def save_approx_rect(self):
        self.config.set_number("Approx", "approx_rect_h", self.approx_rect_h)
        self.config.set_number("Approx", "approx_rect_w", self.approx_rect_w)

    def set_threshold(self, threshold):
        """

        :param threshold: int
        """
        self.threshold = threshold
        self.save_threshold()

    def save_threshold(self):
        self.config.set_number("Approx", "threshold", self.threshold)

    def save_zf(self):
        self.pixelToCMFactor = self.config.set_float("ZF", "pixelToCMFactor", self.pixelToCMFactor)

    def save_config(self):
        self.save_approx_rect()
        self.save_field()
        self.save_threshold()
        print 'config saved'