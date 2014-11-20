from unittest import TestCase
import Test.camera as camera
__author__ = 'endru'


class TestPiCamera(TestCase):
    def test_take_picture(self):
        cam = camera.CamFactory.create_cam('PiCamera')
        pic = cam.take_picture
        self.assertRaises(Exception)
        self.assertIsNotNone(pic, "no picture")

    def test_close(self):
        cam = camera.CamFactory.create_cam('PiCamera')
        cam.close()
        self.assertRaises(Exception)