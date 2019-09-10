import json
import re
import sys
import time
import logging

from queue import Queue
from threading import Thread, Event
from arhuaco.sensors.source.sysdig_metrics import SysdigMetrics
from arhuaco.sensors.sequence_sample import SequenceSample

class SyscallSensor(Thread):

    def __init__(self, parameters, input_queue_dict):
        super(SyscallSensor, self).__init__()
        self.parameters       = parameters
        self.data_source      = None
        self.input_queue      = None
        self.input_queue_dict = input_queue_dict

    def start_collecting(self):
        # Start syscall connection data collection
        sysdig_source = SysdigMetrics(None)
        self.input_queue  = Queue()
        self.input_queue_dict["syscall_sensor"]\
                             = self.input_queue
        self.data_source = sysdig_source.get_data_iterator()
        sequence = SequenceSample(6)
        sequence.bind_to(self.update_samples)
        while True:
            sample = next(self.data_source)
            fields = sample.strip().split()
            # Don't include the container ID nor thread ID
            sequence.set_samples(fields[1], " ".join(fields[2:]))

    def start_collecting_log(self):
        # Start syscall connection data collection
        sysdig_source = SysdigMetrics(None)
        self.data_source = sysdig_source.store_data_in_file("/var/log/arhuaco/sysdig.log")

    def update_samples(self, samples):
        self.input_queue.put(samples)

    def run(self):
        self.start_collecting_log()

    def stop(self):
        self.stoprequest.set()
