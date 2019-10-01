# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from abc import ABCMeta, abstractmethod

# Base class for producing responses to detected
# threats.

class Action:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_action(self):
        pass
