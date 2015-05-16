__author__ = 'endru'
import threading
import picamera
import picamera.array

class ThreadPiCam(threading.Thread):
    class PiCameraException(Exception):
        msg = "PiCameraException: "

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.msg + self.value

    lock1 = threading.Lock()
    lock2 = threading.Lock()
    image = None
    stop_thread = False
    cam_inited = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stop = threading.Event()

        print "threadcam init"
        ThreadPiCam.stop_thread = False
        ThreadPiCam.cam_inited = False
        ThreadPiCam.lock1.acquire()
        ThreadPiCam.lock2.acquire()

        print "threadcam init finished"

    def run(self):
        print "threadcam run"
        with picamera.PiCamera() as camera:
            self.cam = camera
            ThreadPiCam.cam_inited = True
            while not ThreadPiCam.stop_thread:
                print "threadcam while"
                ThreadPiCam.lock1.acquire()
                if ThreadPiCam.stop_thread:
                    print "threadcam stop"
                    break
                try:
                    self.stream = picamera.array.PiRGBArray(camera)
                    camera.capture(self.stream, format='bgr', use_video_port=True)
                    # At this point the image is available as stream.array
                    ThreadPiCam.image = self.stream.array
                    print "picture taken"
                finally:
                    self.stream.truncate()
                ThreadPiCam.lock2.release()
            print "threadcam exit while - stop"

    @property
    def get_height(self):
        return self.height

    @property
    def get_width(self):
        return self.width

    @property
    def take_picture(self):
        print "start take picture"
        ThreadPiCam.lock1.release()
        ThreadPiCam.lock2.acquire()
        print "return picture"
        return ThreadPiCam.image

    def stop(self):
        self._stop.set()
        ThreadPiCam.stop_thread = True
        ThreadPiCam.lock1.release()

    def stopped(self):
        return self._stop.isSet()

    def close(self):
        print "threadcam close"
        self.stop()
        print "threadcam self join"
        self.join()
        print 'threadcam self joined'

    def set_resolution(self, w, h):
        if w > 0:
            self.width = w
        if h > 0:
            self.height = h
        self.cam.resolution = (w, h)

    def __del__(self):
        self.close()
        print 'threadcam object del'

    class Factory():
        def __init__(self):
            pass

        @property
        def create(self):
            thread_cam = ThreadPiCam()
            thread_cam.start()
            return thread_cam