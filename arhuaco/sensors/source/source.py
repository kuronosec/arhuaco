from abc import ABCMeta, abstractmethod

class Source:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data_iterator(self):
        pass
    @abstractmethod
    def get_data_source(self):
        pass
