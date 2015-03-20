__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os


class BDConfig:
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "balldepot.ini"
        self.config = CF.ConfigHandler(self.dirPath + "/" + self.file_name)
        self.timeForBall = self.config.get_float("Balldepot", "timeForBall", 4)
        self.servo_min = self.config.get_number("Balldepot", "servo_min", 150)
        self.servo_max = self.config.get_number("Balldepot", "servo_max", 600)

    def get_timeForBall(self):
        return self.angle2Step

    def set_timeForBall(self, timeForBall):
        self.config.set_float("Balldepot", "timeForBall", timeForBall)
        self.timeForBall = timeForBall

    def set_servo_max(self, servo_max):
        self.config.set_number("Balldepot", "servo_max", servo_max)
        self.servo_max = servo_max

    def set_servo_min(self, servo_min):
        self.config.set_number("Balldepot", "servo_min", servo_min)
        self.servo_min = servo_min
