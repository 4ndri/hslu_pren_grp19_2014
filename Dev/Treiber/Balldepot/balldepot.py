__author__ = 'Andri'
import Dev.Treiber.Balldepot.config as CFG
import Dev.Hardware.Servo.servoContinuous as Servo


class Balldepot:
    def __init__(self):
        self.nbOfBalls = 5
        self.servo = Servo.ContinuousServo(0, 150, 600)
        self.config = CFG.BDConfig()
        print "Balldepot inited"

    @property
    def load(self):
        """

        :rtype : int
        """
        print "Balldepot: load"
        self.servo.turnRight(self.config.timeForBall)
        self.nbOfBalls -= 1
        return self.nbOfBalls

    @property
    def get_config(self):
        return self.config