__author__ = 'Andri'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import Dev.Treiber.Zielerfassung as ZF


class ISteuerung:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def init(self):
        raise NotImplementedError()

    @abstractmethod
    def get_zielerfassung(self):
        raise NotImplementedError()


class Steuerung(ISteuerung):

    def __init__(self):
        """

        :rtype : Steuerung
        """
        self.zielerfassung = ZF.Zielerfassung()

