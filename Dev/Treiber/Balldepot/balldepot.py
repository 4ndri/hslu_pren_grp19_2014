__author__ = 'Andri'
import Dev.Treiber.Balldepot.config as CFG
# import Dev.Hardware.Servo.WiringPiServo as Servo
import Dev.Hardware.Servo.PigpioServo as Servo


class Balldepot:
    def __init__(self):
        self.nbOfBalls = 5
        self.config = CFG.BDConfig()
        self.servo = Servo.ContinuousServo(self.config.duty, self.config.duty, self.config.gpio_pin)
        print "Balldepot inited"

    @property
    def load(self):
        """

        :rtype : int
        """
        print "Balldepot: load"
        if self.nbOfBalls == 5:
            self.servo.turnRight(self.config.timeForBall / 2)
            self.nbOfBalls -= 1
        elif self.nbOfBalls >= 0:
            self.servo.turnRight(self.config.timeForBall)
            self.nbOfBalls -= 1
        else:
            self.servo.turnLeft(self.config.timeForBall / 2)
            self.nbOfBalls = 4
        return self.nbOfBalls

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        print "save balldepot config"
        self.config.save_config()
        self.servo = None
        self.servo = Servo.ContinuousServo(self.config.duty, self.config.duty, self.config.gpio_pin)