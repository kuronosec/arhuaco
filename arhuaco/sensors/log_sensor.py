import json
import re
import sys
import time
import threading
import logging

from queue import Queue
from threading import Thread, Event
from arhuaco.sensors.source.log_metrics import LogMetrics
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
        if self.input_type == "syscall_sensor":
            sequence = SequenceSample(6)
            sequence.bind_to(self.update_samples)
            while True:
                sample = next(self.data_source)
                fields = sample.strip().split()
                # Don't include the container ID nor thread ID
                sequence.set_samples(fields[1], " ".join(fields[2:]))
        elif self.input_type == "network_sensor":
            while True:
                sample = next(self.data_source)
                self.input_queue.put([sample])

    def update_samples(self, samples):
        self.input_queue.put(samples)

    def run(self):
        self.start_data_stream()

    def stop(self):
        pass

    def get_data_source(self):
        return self.data_source
