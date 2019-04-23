import json
import re
import sys
import time
import threading
import logging

from arhuaco.sensors.utils.docker_utils import DockerUtils
from arhuaco.sensors.source.docker_metrics import DockerMetrics
from arhuaco.backend.prometheus import prometheus
from docker.errors import NotFound
from threading import Thread, Event
from queue import Queue, Empty

class DockerSensor(Thread):

    def __init__(self, parameters, input_queue_dict):
        super(DockerSensor, self).__init__()
        self.parameters = parameters
        self.dockerSocketPath = dockerSocketPath
        self.containerId      = containerId
        self.updateInterval   = updateInterval
        self.container        = DockerUtils(self.dockerSocketPath)
        self.data_source      = None
        self.input_queue_dict = input_queue_dict

    def initialize(self):
        # Create docker stats collection services.
        containerInfo = DockerUtils(socketPath)
        start_http_server(8000)
        events_obj = containerInfo.getEvents(filters= {'event': 'start',
                                                         'image': 'test:alien'})
        for event in events_obj:
            monitor = arhuaco(socketPath, event['id'][0:12], updateInterval)
            Thread(target=monitor.start_collecting,
                   name="monitor.start_collecting").start()


    def start_collecting(self):
        logging.info('Creating threads for Container: %s '
                     % self.containerId)
        # Create threads
        docker_metrics_thread = DockerMetrics(self.dockerSocketPath,
                                               self.containerId,
                                               self.updateInterval)
        backend = prometheus(self.containerId, 0, 9091, "iri03", queue=None)
        # get data queues
        queue_docker = docker_metrics_thread.getQueue()
        # Start Theads
        docker_metrics_thread.start()
        Thread(target=backend.write, name='backend.write.pull',
               args=[queue_docker, 'pull']).start()

        while True:
            try:
                if self.isAlive(self.containerId):
                    time.sleep(self.updateInterval)
                else:
                    break
            except NotFound:
                break

        logging.info('Terminating threads for Container: %s ' % self.containerId)
        docker_metrics_thread.stop()
        docker_metrics_thread.join()
        logging.info('End of collecting data for Container: %s ' % self.containerId)

    def start_collecting(self):
        # Start syscall connection data collection
        self.data_source = SysdigMetrics(None)

    def run(self):
        self.start_collecting()

    def stop(self):
        self.stoprequest.set()

    def get_data_source(self):
        return self.data_source
