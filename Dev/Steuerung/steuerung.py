__author__ = 'Andri'
import Dev.Treiber.Zielerfassung.zielerfassungv3 as ZF
import Dev.Treiber.Ballbefoerderung.ballbefoerderung as BF
import Dev.Treiber.Balldepot.balldepot as BD
import Dev.Treiber.Ausrichtung.ausrichtung as AR
import time


class Steuerung:
    def __init__(self):
        """

        :rtype : Steuerung
        """
        self.init()

    def init(self):
        print "Steuerung: init"
        self.balldepot = BD.Balldepot()
        self.zielerfassung = ZF.Zielerfassung()
        self.ballbefoerderung = BF.Ballbefoerderung()
        self.ausrichtung = AR.Ausrichtung()

    def start(self):
        counter = 0
        angle = 5
        self.zielerfassung.dir = 0
        # while counter < 5 and angle > 0.01:
        #     angle = self.zielerfassung.detect()
        #     self.ausrichtung.moveXAngle(angle)

        angle = self.zielerfassung.detect()
        self.ausrichtung.moveXAngle(angle)

        self.ballbefoerderung.run()
        time.sleep(self.balldepot.config.waitTime1)
        while self.balldepot.load > 0:
            time.sleep(self.balldepot.config.waitTimeOther)
        time.sleep(0.1)
        self.ballbefoerderung.stop()

    def reset(self):
        self.ausrichtung.reset()
        self.ballbefoerderung.stop()
        self.balldepot.nbOfBalls = 5
        self.zielerfassung.dir = 0

    def reset_all(self):
        self.balldepot = BD.Balldepot()
        #self.zielerfassung.close()
        self.zielerfassung = ZF.Zielerfassung()
        self.ballbefoerderung = BF.Ballbefoerderung()
        self.ausrichtung = AR.Ausrichtung()

    @property
    def get_zielerfassung(self):
        return self.zielerfassung

    @property
    def get_ausrichtung(self):
        """

        :rtype : AR.Ausrichtung
        """
        return self.ausrichtung

    @property
    def get_ballbefoerderung(self):
        """

        :rtype : BF.Ballbefoerderung
        """
        print "Steuerung: get_ballbefoerderung"
        return self.ballbefoerderung

    @property
    def get_balldepot(self):
        """

        :rtype : BD.Balldepot
        """
        print "Steuerung: get_balldepot"
        return self.balldepot
