__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os


class BDConfig:
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "Balldepot.ini"
        self.config = CF.ConfigHandler(self.dirPath + "/" + self.file_name)
        self.timeForBall = self.config.get_float("Balldepot", "timeForBall", 1)
        self.duty = self.config.get_float("Balldepot", "duty", 1.52)
        self.gpio_pin = self.config.get_number("Balldepot", "gpio_pin", 18)

    def set_timeForBall(self, timeForBall):
        self.timeForBall = timeForBall
        self.config.set_float("Balldepot", "timeForBall", self.timeForBall)

    def set_gpio_pin(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.config.set_number("Balldepot", "gpio_pin", self.gpio_pin)

    def save_config(self):
        self.config.set_float("Balldepot", "timeForBall", self.timeForBall)
        self.config.set_number("Balldepot", "gpio_pin", self.gpio_pin)
        self.config.set_float("Balldepot", "duty", self.duty)
