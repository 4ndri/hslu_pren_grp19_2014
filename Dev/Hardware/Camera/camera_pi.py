__author__ = 'endru'
import picamera
import picamera.array

class PiCamera:
    def __init__(self):
        self.width = 640
        self.height = 480

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    @property
    def take_picture(self):
        try:
            image = None
            with picamera.PiCamera() as camera:
                camera.resolution = (self.width, self.height)
                self.stream = picamera.array.PiRGBArray(camera)
                camera.capture(self.stream, format='bgr', use_video_port=True)
                # At this point the image is available as stream.array
                image = self.stream.array
                print "picture taken"
            return image
        finally:
            self.stream.truncate()

    def close(self):
        # self.cam.close()
        print 'picamera closed'

    def set_resolution(self, w, h):
        if w > 0:
            self.width = w
        if h > 0:
            self.height = h
        with picamera.PiCamera() as camera:
            camera.resolution = (w, h)

    def __del__(self):
        self.close()
        print 'picamera object del'

    class Factory():
        def __init__(self):
            pass

        @property
        def create(self):
            return PiCamera()
