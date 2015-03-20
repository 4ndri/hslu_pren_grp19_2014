from unittest import TestCase
import Dev.Treiber.Ausrichtung.config as AC
__author__ = 'endru'


class TestARConfig(TestCase):
    def test_CreateARConfig(self):
        config=AC.ARConfig()
        config.set_angle2Step(8)
        self.assertEqual(config.angle2Step,8,"test set angle2Step")