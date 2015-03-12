from unittest import TestCase
import Dev.Test.camera as camera
__author__ = 'endru'


class TestCamera(TestCase):
    def test_take_picture(self):
        cam = camera.CamFactory.create_cam('Camera')
        pic = cam.take_picture
        self.assertRaises(Exception)
        self.assertIsNotNone(pic, "no picture")

    def test_close(self):
        cam = camera.CamFactory.create_cam('Camera')
        cam.close()
        self.assertRaises(Exception)