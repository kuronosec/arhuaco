import json
import re
import sys
import time
import threading
import logging

from queue import Queue
from threading import Thread, Event
from arhuaco.sensors.source.log_metrics import LogMetrics

class LogSensor(threading.Thread):

    def __init__(self, parameters, input_queue_dict,
                 input_file, input_type):
        super(LogSensor, self).__init__()
        self.parameters       = parameters
        self.data_source      = None
        self.input_queue      = None
        self.input_queue_dict = input_queue_dict
        self.input_file       = input_file
        self.input_type       = input_type

    def start_data_stream(self):
        # Start network connection data collection
        log_source = LogMetrics(self.input_file)
        self.input_queue = Queue()
        self.input_queue_dict[self.input_type]\
                         = self.input_queue
        self.data_source = log_source.get_data_iterator()
        while True:
            sample = next(self.data_source)
            self.input_queue.put([sample])

    def run(self):
        self.start_data_stream()

    def stop(self):
        pass

    def get_data_source(self):
        return self.data_source
