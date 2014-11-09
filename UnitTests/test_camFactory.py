from unittest import TestCase
import Test.camera as camera
__author__ = 'endru'


class TestCamFactory(TestCase):
    def test_add_factory(self):
        fac = camera.Camera.Factory(0)
        camera.CamFactory.add_factory("Camera", fac)
        self.assertRaises(Exception)

    def test_create_cam(self):
        cam = camera.CamFactory.create_cam
        self.assertRaises(Exception)
