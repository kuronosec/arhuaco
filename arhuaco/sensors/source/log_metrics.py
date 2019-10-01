# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import sys
import time
import subprocess
import logging
import os.path
import time

from arhuaco.sensors.source.source import Source

class LogMetrics(Source):

    def __init__(self, dataPath):
        # Initialize entities
        super(LogMetrics, self).__init__()
        self.dataPath        = dataPath

    def get_data_iterator(self):
        # Collect data from log file
        command_log = ("tail -f %s" % self.dataPath)
        while not os.path.exists(self.dataPath):
            time.sleep(1)
        logging.info("Starting the log collection %s" % command_log)
        proc_log = subprocess.Popen(command_log,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
        # Extract data from the logs
        while proc_log.poll() is None:
            line = proc_log.stdout.readline()
            yield line.decode('utf-8')
        logging.info(proc_log.poll())
        logging.info('Finalyzing log collection.')
        proc_log.terminate()

    def get_data_source(self):
        return None
