import sys
import time
import subprocess
import logging
import os.path
import time

from arhuaco.sensors.source.source import Source

class NetworkMetrics(Source):

    def __init__(self, dataPath=None):
        # Initialize entities
        super(NetworkMetrics, self).__init__()
        self.dataPath        = dataPath

    def get_data_iterator(self):
        # Collect network data by the bro network analyzer
        logging.info("Start network collection.")
        command_bro = ("broctl start")
        command_log = (" tail -f /var/log/bro/current/dns.log ")
        logging.info("Starting BRO %s" % command_bro)
        proc_bro = subprocess.Popen(["broctl","start"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        while not os.path.exists("/var/log/bro/current/dns.log"):
            time.sleep(1)
        logging.info("Starting the log collection %s" % command_log)
        proc_log = subprocess.Popen(command_log,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
        # Extract data from the BRO logs
        while proc_log.poll() is None:
            line = proc_log.stdout.readline()
            yield self.filter(line)
        logging.info(proc_log.poll())
        logging.info('Finalyzing BRO collection.')
        proc_bro.terminate()
        logging.info('Finalyzing log analysis.')
        proc_log.terminate()

    def store_data_in_file(self):
        # Collect network data by the bro (zeek) network analyzer
        logging.info("Start network collection.")
        command_bro = ("broctl start")
        command_log = (" tail -f /var/log/bro/current/dns.log ")
        logging.info("Starting zeek %s" % command_bro)
        proc_bro = subprocess.Popen(["broctl","start"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        while not os.path.exists("/var/log/bro/current/dns.log"):
            time.sleep(1)
        logging.info("zeek started...")

    def get_data_source(self):
        return None

    def filter(self, string):
        fields = string.strip().split("\x09")
        line = ""
        if len(fields) > 5:
            line = fields[1]+" "+fields[2]+" "+fields[3]\
                   +" "+fields[4]+" "+fields[5]
        return line
