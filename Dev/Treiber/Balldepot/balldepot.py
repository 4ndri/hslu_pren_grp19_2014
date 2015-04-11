__author__ = 'Andri'
import Dev.Treiber.Balldepot.config as CFG
import Dev.Hardware.Servo.servoContinuous as Servo
import Dev.Hardware.Servo.WiringPiServo as WServo


class Balldepot:
    def __init__(self):
        self.nbOfBalls = 5
        self.config = CFG.BDConfig()
        self.wservo = WServo.ContinuousServo(self.config.servo_max, self.config.freq)
        # self.servo = Servo.ContinuousServo(self.config.channel, self.config.servo_min, self.config.servo_max, self.config.freq)
        print "Balldepot inited"

    @property
    def load(self):
        """

        :rtype : int
        """
        print "Balldepot: load"
        if self.nbOfBalls >= 0:
            # self.servo.turnRight(self.config.timeForBall)
            self.wservo.turnRight(self.config.timeForBall)
            self.nbOfBalls -= 1
        else:
            # self.servo.turnLeft(self.config.timeForBall)
            self.wservo.turnLeft(self.config.timeForBall)
            self.nbOfBalls += 1
        return self.nbOfBalls

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        print "save balldepot config"
        self.config.save_config()
        self.wservo = None
        self.wservo = WServo.ContinuousServo(self.config.freq, self.config.duty_min, self.config.duty_max)
        #self.servo = Servo.ContinuousServo(self.config.channel, self.config.servo_max, self.config.servo_max, self.config.freq)