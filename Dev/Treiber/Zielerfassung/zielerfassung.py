__author__ = 'Andri'

from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import math

import Dev.Treiber.Zielerfassung.config as CFG
import Dev.Treiber.Zielerfassung.ContourFinder as CF
import Dev.Hardware.Camera.camera as camera


class IZielerfassung:
    __metaclass__ = ABCMeta

    @abstractproperty
    def detect(self):
        raise NotImplementedError()

    @abstractmethod
    def get_threshold(self):
        raise NotImplementedError()

    @abstractmethod
    def set_threshold(self, threshold):
        raise NotImplementedError()

    @abstractproperty
    def get_image(self):
        raise NotImplementedError()

    @abstractmethod
    def set_field(self):
        raise NotImplementedError()


class Zielerfassung(IZielerfassung):
    def __init__(self):
        try:
            self.cam = camera.get_camera()
            self.config = CFG.ZFConfig()
            self.cntCalc = CF.ContourCalc(self.config)
            self.cam.set_resolution(self.config.resolution_w, self.config.resolution_h)
        except Exception as ex:
            print ex.message

    @property
    def detect(self):
        img = self.cam.take_picture
        cnt_info = self.cntCalc.find_contours(img, False)
        position = cnt_info.center_distance.x
        angle = math.atan(self.config.pixelToCMFactor * position)
        print "position: pixel: " + str(position) + "   angle: " + str(angle)
        return position

    def get_threshold(self):
        return self.config.threshold

    def set_threshold(self, threshold):
        self.config.set_threshold(threshold)

    @property
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
