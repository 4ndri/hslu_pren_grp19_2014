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
from Dev.Test.video import create_capture
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
            fac = eval(name+'.Factory()')
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
        self.cam = create_capture(video_src)
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




class PiCamera(ICamera):
    class PiCameraException(Exception):
        msg="PiCameraException: "
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.msg + self.value

    def __init__(self):
        if pi_cam_available:
            self.cam = picamera.PiCamera()
            self.stream = io.BytesIO()
        else:
            raise PiCamera.PiCameraException("initialization failed")

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    @property
    def take_picture2(self):
        self.cam.capture(self.stream, format="jpeg", use_video_port=True)
        frame = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
        self.stream.seek(0)
        frame = cv2.imdecode(frame, 1)
        return frame

    @property
    def take_picture(self):
        try:
            image = None
            self.stream = picamera.array.PiRGBArray(self.cam)
            self.cam.capture(self.stream, format='bgr', use_video_port=True)
            # At this point the image is available as stream.array
            image = self.stream.array
            return image
        finally:
            self.stream.truncate()



    def close(self):
        self.cam.close()
        print 'picamera closed'

    def set_resolution(self, w, h):
        self.cam.resolution = (w, h)

    def __del__(self):
        self.close()
        print 'picamera object del'

    class Factory(AbstractFactory):
        def __init__(self):
            pass

        @property
        def create(self):
            return PiCamera()


class PiCamera2(ICamera):
    class PiCameraException(Exception):
        msg="PiCameraException: "
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.msg + self.value

    def __init__(self):
        if pi_cam_available:
            self.stream = io.BytesIO()
        else:
            raise PiCamera.PiCameraException("initialization failed")

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    @property
    def take_picture2(self):
        self.cam.capture(self.stream, format="jpeg", use_video_port=True)
        frame = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
        self.stream.seek(0)
        frame = cv2.imdecode(frame, 1)
        return frame

    @property
    def take_picture(self):
        try:
            image = None
            with picamera.PiCamera() as camera:
                self.stream = picamera.array.PiRGBArray(camera)
                self.cam.capture(self.stream, format='bgr', use_video_port=True)
                # At this point the image is available as stream.array
                image = self.stream.array
            return image
        finally:
            self.stream.truncate()



    def close(self):
        #self.cam.close()
        print 'picamera closed'

    def set_resolution(self, w, h):
        with picamera.PiCamera() as camera:
            camera.resolution = (w, h)

    def __del__(self):
        self.close()
        print 'picamera object del'

    class Factory(AbstractFactory):
        def __init__(self):
            pass

        @property
        def create(self):
            return PiCamera2()

def get_camera():
    """

    :rtype : ICamera
    """
    camera = None
    if pi_cam_available:
        print "picamera available"
        camera = CamFactory.create_cam('PiCamera2')
    else:
        camera = CamFactory.create_cam('Camera')
    return camera
