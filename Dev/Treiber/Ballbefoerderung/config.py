__author__ = 'endru'
import Dev.Config.ConfigHandler as CF
import os


class BFConfig:
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "Ballbefoerderung.ini"
        self.config = CF.ConfigHandler(self.dirPath + "/" + self.file_name)
        self.pulse_length = self.config.get_float("Ballbefoerderung", "pulse_length", 0.5)
        self.channel = self.config.get_number("Ballbefoerderung", "channel", 0)
        self.freq = self.config.get_number("Ballbefoerderung", "freq", 1000)

    def get_pulse_length(self):
        return self.pulse_length

    def set_pulse_length(self, pulse_length):
        self.pulse_length = pulse_length
        self.config.set_float("Ballbefoerderung", "timeForBall", self.pulse_length)

    def set_freq(self, freq):
        self.freq = freq
        self.config.set_number("Ballbefoerderung", "freq", self.freq)

    def set_channel(self, channel):
        self.channel=channel
        self.config.set_number("Ballbefoerderung", "channel", self.channel)

    def save_config(self):
        self.config.set_float("Ballbefoerderung", "pulse_length", self.pulse_length)
        self.config.set_number("Ballbefoerderung", "channel", self.channel)
        self.config.set_number("Ballbefoerderung", "freq", self.freq)
