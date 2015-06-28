#!/usr/bin/env python
# from docutils.writers import null

__author__ = 'endru'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import numpy as np
import cv2
import cv2.cv as cv
import io
import time

try:
    import picamera
    import picamera.array

    pi_cam_available = True
except ImportError:
    pi_cam_available = False


class AbstractFactory:
    __metaclass__ = ABCMeta

    @abstractproperty
    def create(self):
        """creates an object defined in the specific factory implementation"""
        raise NotImplementedError()


class CamFactory:
    factories = {}

    def add_factory(name, factory):
        CamFactory.factories[name] = factory

    add_factory = staticmethod(add_factory)
    # A Template Method:

    def create_cam(name):
        """

        :rtype : ICamera
        """
        if not CamFactory.factories.has_key(name):
            fac = eval(name + '.Factory()')
            CamFactory.add_factory(name, fac)
        return CamFactory.factories[name].create

    create_cam = staticmethod(create_cam)


class ICamera:
    __metaclass__ = ABCMeta

    @abstractproperty
    def get_height(self):
        return self.height

    @abstractproperty
    def get_width(self):
        return self.width

    @abstractproperty
    def take_picture(self):
        """

        :rtype : np.ndarray
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def set_resolution(self, w, h):
        raise NotImplementedError()


class Camera(ICamera):
    def __init__(self, video_src=0):
        self.video_src = video_src
        self.cam = cv2.VideoCapture(video_src)
        #self.cam = create_capture(video_src)
        # self.height = 480
        # self.width = 640
        # self.set_resolution()
        time.sleep(2)

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    @property
    def take_picture(self):
        """

        :rtype : np.numpy.array
        """
        ret, img = self.cam.read()
        if not ret:
            print "camera: error taking picture"
        return img

    def close(self):
        self.cam.release()
        print 'camera closed'

    def set_resolution(self, w=0, h=0):
        if w > 0:
            self.width = w
        if h > 0:
            self.height = h
        # cv.SetCaptureProperty(self.cam, cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.height)

    def __del__(self):
        self.close()
        print 'camera object del'

    class Factory(AbstractFactory):
        def __init__(self, video_src=0):
            self.video_src = video_src

        @property
        def create(self):
            return Camera(self.video_src)





def get_camera():
    """

    :rtype : ICamera
    """
    camera = None
    try:
        if pi_cam_available:
            print "picamera available"
            camera = CamFactory.create_cam('ThreadPiCam')
        else:
            camera = CamFactory.create_cam('Camera')
    finally:
        return camera
