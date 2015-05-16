__author__ = 'Andri'

from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import math

import Dev.Treiber.Zielerfassung.config as CFG
import Dev.Treiber.Zielerfassung.ContourFinder as CF
import Dev.Hardware.Camera.camera as camera
import Dev.Hardware.Camera.thread_camera as th_cam
import time


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
            self.dir = 0
            self.cam = camera.Camera(0)
            #self.cam=th_cam.ThreadPiCam()
            #self.cam.start()
            self.config = CFG.ZFConfig()
            self.cntCalc = CF.ContourCalc(self.config)
            #self.cam.set_resolution(self.config.resolution_w, self.config.resolution_h)
        except Exception as ex:
            print ex.message

    @property
    def detect(self):
        t = time.time()
        img = self.cam.take_picture
        cnt_info = self.cntCalc.find_contours(img,self.dir, False, False)
        self.dir = cnt_info.prev_dir
        position = cnt_info.center_distance.x
        angle = math.atan(self.config.pixelToCMFactor * position)
        dt = time.time() - t
        print "position: pixel: " + str(position) + "  |  angle: " + str(angle) + "  |  time: " + str(dt * 1000)
        return angle

    def get_threshold(self):
        return self.config.threshold

    def set_threshold(self, threshold):
        self.config.set_threshold(threshold)

    @property
    def get_image(self):
        t = time.time()
        img = self.cam.take_picture
        cnt_info = self.cntCalc.find_contours(img, self.dir, True, False)
        position=0
        if cnt_info is not None:
            print "zf: no object found"
            self.dir = cnt_info.prev_dir
            position = cnt_info.center_distance.x
        angle = math.atan(self.config.pixelToCMFactor * position)
        dt = time.time() - t
        print "position: pixel: " + str(position) + "  |  angle: " + str(angle) + "  |  time: " + str(dt * 1000)
        return cnt_info

    def set_field(self):
        raise NotImplementedError()

    def save_config(self):
        self.config.save_config()
        self.cntCalc = None
        self.cntCalc = CF.ContourCalc(self.config)
        self.cam.set_resolution(self.config.resolution_w, self.config.resolution_h)

    def close(self):
        self.cam.close()


