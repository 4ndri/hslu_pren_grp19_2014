__author__ = 'bof'

from abc import ABCMeta, abstractproperty, abstractmethod

class IZielerfassung:
    __metaclass__ = ABCMeta

    @abstractproperty
    def detect(self):
        raise NotImplementedError()

    @abstractmethod
    def get_threshold(self):
        raise NotImplementedError()

    @abstractmethod
    def set_threshold(self, threshold):
        raise NotImplementedError()

    @abstractproperty
    def get_image(self):
        raise NotImplementedError()

    @abstractmethod
    def set_field(self):
        raise NotImplementedError()