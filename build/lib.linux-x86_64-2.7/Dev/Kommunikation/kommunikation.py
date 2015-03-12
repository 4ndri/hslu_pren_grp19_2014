__author__ = 'Andri'

class IKommunikation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, message):
        raise NotImplementedError()

    @abstractmethod
    def receive(self, message):
        raise NotImplementedError()

    @abstractmethod
    def setup(self, config):
        raise NotImplementedError()

    @abstractmethod
    def connect(self, config):
        raise NotImplementedError()


class Kommunikation(IKommunikation):
    def __init__(self):
        bla=123

    def setup(self,config):
        raise NotImplementedError()

    def receive(self, message):
        raise NotImplementedError()

    def send(self, message):
        raise NotImplementedError()