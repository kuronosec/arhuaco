# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import json
import re
import sys
import time
import threading
import logging

from queue import Queue
from threading import Thread, Event
from arhuaco.sensors.source.network_metrics import NetworkMetrics

class NetworkSensor(threading.Thread):

    def __init__(self, parameters, input_queue_dict):
        super(NetworkSensor, self).__init__()
        self.parameters       = parameters
        self.data_source      = None
        self.input_queue      = None
        self.input_queue_dict = input_queue_dict

    def collect_from_source(self):
        # Start network connection data collection
        network_source = NetworkMetrics(None)
        self.input_queue = Queue()
        self.input_queue_dict["network_sensor"]\
                         = self.input_queue
        self.data_source = network_source.get_data_iterator()
        while True:
            sample = next(self.data_source)
            self.input_queue.put([sample])

    def start_collecting_log(self):
        # Start network connection data collection
        network_source = NetworkMetrics(None)
        self.data_source = network_source.store_data_in_file()

    def run(self):
        self.start_collecting_log()

    def stop(self):
        pass

    def get_data_source(self):
        return self.data_source
