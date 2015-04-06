__author__ = 'Andri'
import Dev.Treiber.Balldepot.config as CFG
import Dev.Hardware.Servo.servoContinuous as Servo
import Dev.Hardware.Servo.PWMKernelServo as KServo


class Balldepot:
    def __init__(self):
        self.nbOfBalls = 5
        self.config = CFG.BDConfig()
        self.kservo = KServo.ContinuousServo(180)
        self.servo = Servo.ContinuousServo(self.config.channel, self.config.servo_min, self.config.servo_max, self.config.freq)
        print "Balldepot inited"

    @property
    def load(self):
        """

        :rtype : int
        """
        print "Balldepot: load"
        self.servo.turnRight(self.config.timeForBall)
        self.kservo.turnRight(self.config.timeForBall)
        self.nbOfBalls -= 1
        return self.nbOfBalls

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        self.config.save_config()
        self.servo = Servo.ContinuousServo(self.config.channel, self.config.servo_max, self.config.servo_max, self.config.freq)