__author__ = 'Andri'

from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod

import Dev.Treiber
import Dev.Hardware.Camera as camera

class IZielerfassung:
    __metaclass__ = ABCMeta

    @abstractproperty
    def get_position(self):
        raise NotImplementedError()

    @abstractmethod
    def get_threshold(self):
        raise NotImplementedError()

    @abstractmethod
    def set_threshold(self, threshold):
        raise NotImplementedError()

    @abstractmethod
    def get_image(self):
        raise NotImplementedError()

    @abstractmethod
    def set_field(self):
        raise NotImplementedError()

class Zielerfassung(IZielerfassung):
    def __init__(self):
        self.cam = camera.get_camera()
        self.config = Zielerfassung.MyConfig()
        self.cntCalc = Zielerfassung.ContourCalc(self.config)
        self.cam.set_resolution(self.config.resolution_w,self.config.resolution_h)

    @property
    def get_position(self):
        img = self.cam.take_picture
        cnt_info = self.cnt_calculator.find_contours(img)
        position = cnt_info.center_distance.x
        return position
