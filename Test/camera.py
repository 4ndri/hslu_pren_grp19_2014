__author__ = 'endru'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import numpy as np
import cv2
import io
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
    def addFactory(id, shapeFactory):
        CamFactory.factories.put[id] = shapeFactory
    addFactory = staticmethod(addFactory)
    # A Template Method:
    def createCam(id):
        if not CamFactory.factories.has_key(id):
            CamFactory.factories[id] = \
              eval(id + '.Factory()')
        return CamFactory.factories[id].create()
    createCam = staticmethod(createCam)


class ICamera:
    __metaclass__ = ABCMeta

    @abstractproperty
    def take_picture(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()



class Camera(ICamera):
    def __init__(self, video_src=0):
        self.video_src = video_src
        self.cam = None
        self.cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')

    def take_picture(self):
        pass

    def close(self):
        self.cam.release()

    def __del__(self):
        self.close()
        print self.id, 'del'

    class Factory(AbstractFactory):
        def __init__(self, video_src):
            self.video_src=video_src

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
    def take_picture(self):
        self.cam.capture(self.stream, format="jpeg", use_video_port=True)
        frame = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
        self.stream.seek(0)
        frame = cv2.imdecode(frame, 1)
        return frame

    def close(self):
        self.cam.close()

    def __del__(self):
        self.close()
        print self.id, 'del'

