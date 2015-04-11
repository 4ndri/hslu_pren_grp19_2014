__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os


class BDConfig:
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "Balldepot.ini"
        self.config = CF.ConfigHandler(self.dirPath + "/" + self.file_name)
        self.timeForBall = self.config.get_float("Balldepot", "timeForBall", 4)
        self.servo_min = self.config.get_number("Balldepot", "servo_min", 150)
        self.servo_max = self.config.get_number("Balldepot", "servo_max", 600)
        self.duty_min = self.config.get_float("Balldepot", "duty_min", 1.4)
        self.duty_max = self.config.get_float("Balldepot", "duty_max", 1.6)

        self.channel = self.config.get_number("Balldepot", "channel", 0)
        self.freq = self.config.get_number("Balldepot", "freq", 50)

    def get_timeForBall(self):
        return self.angle2Step

    def set_timeForBall(self, timeForBall):
        self.timeForBall = timeForBall
        self.config.set_float("Balldepot", "timeForBall", self.timeForBall)

    def set_servo_max(self, servo_max):
        self.servo_max = servo_max
        self.config.set_number("Balldepot", "servo_max", self.servo_max)

    def set_servo_min(self, servo_min):
        self.servo_min = servo_min
        self.config.set_number("Balldepot", "servo_min", self.servo_min)

    def set_channel(self, channel):
        self.channel=channel
        self.config.set_number("Balldepot", "channel", self.channel)

    def save_config(self):
        self.config.set_float("Balldepot", "timeForBall", self.timeForBall)
        self.config.set_number("Balldepot", "servo_min", self.servo_min)
        self.config.set_number("Balldepot", "servo_max", self.servo_max)
        self.config.set_number("Balldepot", "channel", self.channel)
        self.config.set_number("Balldepot", "freq", self.freq)
        self.config.set_float("Balldepot", "duty_min", self.duty_min)
        self.config.set_float("Balldepot", "duty_max", self.duty_max)
