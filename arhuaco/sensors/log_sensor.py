import json
import re
import sys
import time
import threading
import logging

from queue import Queue
from threading import Thread, Event
from arhuaco.sensors.source.log_metrics import LogMetrics
from arhuaco.sensors.source.sysdig_metrics import SysdigMetrics
from arhuaco.sensors.source.network_metrics import NetworkMetrics
from arhuaco.sensors.sequence_sample import SequenceSample

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
        # Start log connection data collection
        log_source = LogMetrics(self.input_file)
        self.input_queue = Queue()
        self.input_queue_dict[self.input_type]\
                         = self.input_queue
        self.data_source = log_source.get_data_iterator()
        number_lines = 0
        filter_line_function = None
        if self.input_type == "syscall_sensor":
            number_lines = 6
            filter_line_function = SysdigMetrics().filter
        elif self.input_type == "network_sensor":
            number_lines = 1
            filter_line_function = NetworkMetrics().filter
        sequence = SequenceSample(number_lines)
        sequence.bind_to(self.update_samples)
        while True:
            line = filter_line_function(next(self.data_source))
            fields = line.strip().split()
            # Separate the line between id and data
            sequence.set_samples(fields[0], " ".join(fields[1:]))

    def update_samples(self, samples):
        self.input_queue.put(samples)

    def run(self):
        self.start_data_stream()

    def stop(self):
        pass

    def get_data_source(self):
        return self.data_source
