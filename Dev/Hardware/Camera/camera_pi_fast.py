__author__ = 'endru'
import picamera
import picamera.array
import io

class PiCamera:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.cam = picamera.PiCamera()
        self.stream = io.BytesIO()
        self.cam.resolution = (self.width, self.height)

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    # @property
    # def take_picture2(self):
    #     self.cam.capture(self.stream, format="jpeg", use_video_port=True)
    #     frame = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
    #     self.stream.seek(0)
    #     frame = cv2.imdecode(frame, 1)
    #     return frame

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
        self.width=w
        self.height=h
        self.cam.resolution = (w, h)

    def __del__(self):
        self.close()
        print 'picamera object del'


