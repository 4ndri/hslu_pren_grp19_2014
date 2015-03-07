__author__ = 'Andri'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import Dev.Treiber.Zielerfassung.zielerfassung as ZF


class ISteuerung:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def init(self):
        raise NotImplementedError()

    @abstractproperty
    def get_zielerfassung(self):
        raise NotImplementedError()


class Steuerung(ISteuerung):

    def __init__(self):
        self.init()


    def init(self):
        self.zielerfassung = ZF.Zielerfassung()


    def get_zielerfassung(self):
        return None

    def start(self):
        raise NotImplementedError()
