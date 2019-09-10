import json
import re
import sys
import time
import threading
import subprocess
import logging

from arhuaco.sensors.source.source import Source

class SysdigMetrics(Source):

    def __init__(self, data_path):
        # Initialize entities
        super(SysdigMetrics, self).__init__()
        self.data_path = data_path

    def get_data_iterator(self):
        # Get container sysdig statistics from the available sources
        command = ("sysdig -p'%container.id %thread.tid %evt.category"
                    " %evt.type %evt.args'"
                    " evt.category!= sleep and evt.category!=wait"
                    " and evt.category!=IPC"
                    " and evt.category!=ipc and evt.category!=scheduler"
                    " and container.name contains alien")
        logging.info("Collecting syscalls data %s" % command)
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        while proc.poll() is None:
            line = proc.stdout.readline()
            # logging.info("Captured line: "+line)
            # logging.info("Error line: "+error)
            yield line.decode('utf-8')
        logging.info(proc.poll())
        logging.info('Finalyzing sysdig stats Container.')
        proc.terminate()

    def store_data_in_file(self, log_file):
        # Get container sysdig statistics from the available sources
        command = ("sysdig -C 1024 -w %s/trace.scap -p'%%container.id"
                    " %%evt.category %%evt.type %%evt.args'"
                    " evt.category!= sleep and evt.category!=wait"
                    " and evt.category!=IPC"
                    " and evt.category!=ipc and evt.category!=scheduler"
                    " and container.name contains alien" % log_file)
        logging.info("Collecting syscalls data %s" % command)
        proc = subprocess.Popen(command, shell=True)
        proc.wait()
        logging.info('Finalyzing sysdig stats Container.')
        proc.terminate()

    def get_data_source(self):
        return None
