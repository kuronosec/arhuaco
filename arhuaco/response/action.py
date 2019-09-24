from abc import ABCMeta, abstractmethod

class Action:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_action(self):
        pass
