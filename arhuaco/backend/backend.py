from abc import ABCMeta, abstractmethod

class backend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def setQueue(self, queue, type):
        pass
    @abstractmethod
    def write(self):
        pass
