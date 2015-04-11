__author__ = 'Andri'
import Dev.Treiber.Ballbefoerderung.config as CFG
import Dev.Hardware.DCMotor.BoardDC as DCMotor


class Ballbefoerderung:
    def __init__(self):
        self.config = CFG.BFConfig()
        self.dcMotor = DCMotor.DCController(self.config.channel, self.config.pulse_length, self.config.freq)
        print "Ballbefoerderung inited"

    @property
    def run(self):
        self.dcMotor.run()
        print "Ballbefoerderung run"

    def set_speed(self, pulse_length):
        self.config.set_pulse_length(pulse_length)
        self.dcMotor.set_pulse_length(self.config.pulse_length)

    def stop(self):
        self.dcMotor.stop()
        print "Ballbefoerderung stop"

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        self.config.save_config()
        self.dcMotor =None
        self.dcMotor = DCMotor.DCController(self.config.channel, self.config.pulse_length, self.config.freq)