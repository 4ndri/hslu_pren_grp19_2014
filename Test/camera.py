from docutils.writers import null

__author__ = 'endru'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import numpy as np
import cv2
import cv2.cv as cv
import io
import time
from video import create_capture
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
    def take_picture(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def set_resolution(self,w,h):
        raise NotImplementedError()


class Camera(ICamera):
    def __init__(self, video_src=0):
        self.video_src = video_src
        self.cam = None
        self.cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
        self.height = 480
        self.width = 640
        # self.set_resolution()
        # time.sleep(2)

    def take_picture(self):
        ret, img = self.cam.read()
        return img

    def close(self):
        self.cam.release()

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
        print 'del'

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
    def take_picture3(self):
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
            self.cam.capture(self.stream, format='bgr')
            # At this point the image is available as stream.array
            image = self.stream.array
            return image
        finally:
            self.stream.truncate()

    def close(self):
        self.cam.close()

    def set_resolution(self,w,h):
        pass

    def __del__(self):
        self.close()
        print 'del'

    class Factory(AbstractFactory):
        def __init__(self):
            pass

        @property
        def create(self):
            return PiCamera()


def get_camera():
    """

    :rtype : ICamera
    """
    camera = None
    if pi_cam_available:
        camera = CamFactory.create_cam('PiCamera')
    else:
        camera = CamFactory.create_cam('Camera')
    return camera

