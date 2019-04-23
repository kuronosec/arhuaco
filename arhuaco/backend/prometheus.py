from prometheus_client import start_http_server,\
     Gauge, Counter, CollectorRegistry, push_to_gateway
import random
import time
import datetime
from backend import backend
from queue import Queue, Empty

class prometheus(backend):

    def __init__(self, containerId, portPull,
                 portPush, pushServer, queue):
        self.containerId = containerId
        self.queue       = queue
        self.portPull    = portPull
        self.portPush    = portPush
        self.pushServer  = pushServer
        self.registry    = None
        if self.portPull is not 0:
            start_http_server(self.portPull)

    def setQueue(self, queue):
        self.queue = queue

    def write(self, queue_aux, type):
        if queue_aux is not None:
            self.queue = queue_aux
        if type == 'pull':
            prom_type = Gauge("Job_%s" % self.containerId,
                              "Job metrics", ['metric'])
            self.writePullData(self.queue, prom_type)
        elif type == 'push':
            self.registry = CollectorRegistry()
            prom_type = Gauge('system_call',
                              'Registered system call',
                              ['timestamp'], registry=self.registry)
            self.writePushData(self.queue, prom_type)

    def writePullData(self, queue, prom_type):
        while True:
            try:
                data = queue.get(True, 40)
                for key, value in data.iteritems():
                    prom_type.labels(key).set(value)
            except Empty:
                break

    def writePushData(self, queue, prom_type):
        while True:
            try:
                prom_type.labels(datetime.datetime.now()).set(queue.get(True, 10))
                push_to_gateway(self.pushServer+":"+str(self.portPush),
                                job='arhuaco',
                                registry=self.registry)
            except Empty:
                break

