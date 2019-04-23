import json
import re
import sys
import time
import threading
import logging

# from arhuaco.sensors.util.docker_utils import DockerUtils
# from arhuaco.sensors.docker_sensor import DockerSensor
from arhuaco.sensors.syscall_sensor import SyscallSensor
from arhuaco.sensors.network_sensor import NetworkSensor

class ArhuacoSensors:

    def __init__(self, input_queue_dict):
        self.docker_socket_path = None
        self.container_id       = None
        self.update_interval    = 0
        self.container          = None
        self.configuration      = self.analyze_config_file()
        self.input_queue_dict   = input_queue_dict

    def start_sensors(self):
        # Create sensor instances
        # docker_sensor_thread  = DockerSensor(self.configuration,
        #                                     self.input_queue_dict)
        syscall_sensor_thread = SyscallSensor(self.configuration,
                                              self.input_queue_dict)
        network_sensor_thread = NetworkSensor(self.configuration,
                                              self.input_queue_dict)
        # Start the sensors
        # docker_sensor_thread.start()
        logging.info('Syscall sensor starting')
        syscall_sensor_thread.start()
        logging.info('Network sensor starting')
        network_sensor_thread.start()
        logging.info("Sensors started")
        return

    def analyze_config_file(self):
        self.docker_socket_path = 'unix://var/run/docker.sock'
        self.container_id       = 0
        self.update_interval    = 60
        return None
