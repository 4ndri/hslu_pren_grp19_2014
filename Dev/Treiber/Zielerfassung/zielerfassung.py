from Dev.Treiber.Zielerfassung.IZielerfassung import IZielerfassung

__author__ = 'Andri'

import math

import Dev.Treiber.Zielerfassung.config as CFG
import Dev.Treiber.Zielerfassung.ContourFinder as CF
import Dev.Hardware.Camera.camera as camera


class Zielerfassung(IZielerfassung):
    def __init__(self):
        try:
            self.dir = 0
            self.cam = camera.PiCamera()
            self.config = CFG.ZFConfig()
            self.cntCalc = CF.ContourCalc(self.config)
            self.cam.set_resolution(self.config.resolution_w, self.config.resolution_h)
        except Exception as ex:
            print ex.message

    def detect(self):
        img = self.cam.take_picture
        cnt_info = self.cntCalc.find_contours(img, False)
        position = cnt_info.center_distance.x
        if self.dir == 0:
            if cnt_info.center_distance.x < 0:
                self.dir = -1
            elif cnt_info.center_distance.x > 0:
                self.dir = 1
            else:
                self.dir = 0
        if self.dir < 0:
            right_x = cnt_info.rect.x + cnt_info.rect.width
            position = (right_x - int(float(self.config.approx_rect_w) / 2)) - cnt_info.m_field.x
        else:
            left_x = cnt_info.rect.x
            position = (left_x + int(float(self.config.approx_rect_w) / 2)) - cnt_info.m_field.x
        angle = math.atan(self.config.pixelToCMFactor * position)
        print "position: pixel: " + str(position) + "   angle: " + str(angle)
        return angle

    def get_threshold(self):
        return self.config.threshold

    def set_threshold(self, threshold):
        self.config.set_threshold(threshold)

    def get_image(self):
        img = self.cam.take_picture
        cnt_info = self.cntCalc.find_contours(img, True, False)
        print "position: " + str(cnt_info.center_distance.x)
        return cnt_info

    def set_field(self):
        raise NotImplementedError()

    def save_config(self):
        self.config.save_config()
        self.cntCalc = None
        self.cntCalc = CF.ContourCalc(self.config)
        self.cam.set_resolution(self.config.resolution_w, self.config.resolution_h)
