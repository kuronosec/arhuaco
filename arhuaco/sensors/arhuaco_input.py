# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import json
import re
import sys
import time
import threading
import logging

from arhuaco.sensors.log_sensor import LogSensor
from arhuaco.sensors.rest_sensor import RestSensor

class ArhuacoInput:

    def __init__(self, input_queue_dict):
        self.docker_socket_path = None
        self.container_id       = None
        self.update_interval    = 0
        self.container          = None
        self.configuration      = self.analyze_config_file()
        self.input_queue_dict   = input_queue_dict

    def start_collecting_from_input(self):
        # Create input instances
        syscall_input_thread = LogSensor(self.configuration,
                                          self.input_queue_dict,
                                          "/var/log/arhuaco/sysdig.log",
                                          "syscall_sensor")
        network_input_thread = LogSensor(self.configuration,
                                          self.input_queue_dict,
                                          "/var/log/bro/current/dns.log",
                                          "network_sensor")
        rest_input_thread = RestSensor(self.configuration,
                                        self.input_queue_dict,
                                        "metron_sensor")
        # Start the input
        logging.info('Syscall input starting...')
        syscall_input_thread.start()
        logging.info('Network input starting...')
        network_input_thread.start()
        logging.info('Web REST input starting...')
        rest_input_thread.start()
        logging.info("Input started.")
        return

    def analyze_config_file(self):
        self.docker_socket_path = 'unix://var/run/docker.sock'
        self.container_id       = 0
        self.update_interval    = 60
        return None
