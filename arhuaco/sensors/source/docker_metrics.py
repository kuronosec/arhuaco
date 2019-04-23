import json
import re
import sys
import time
import threading
import logging
import subprocess

from arhuaco.sensor.util.docker_utils import DockerUtils
from arhuaco.sensor.source import Source
from docker.errors import NotFound
from queue import Queue

class DockerMetrics(Source, threading.Thread):

    def __init__(self, socketPath, containerId, update_interval):
        super(DockerMetrics, self).__init__()
        self._socketPath        = socketPath
        self._container         = DockerUtils(socketPath)
        self.containerId        = containerId
        self.queue              = Queue()
        self.update_interval    = update_interval
        self.stoprequest        = threading.Event()

    def getData(self):
        # Get container statistics from the available sources
        logging.info('Analyzing docker stats container: %s ' % self.containerId)
        jobid = None
        while not self.stoprequest.isSet():
            try:
                json_obj = self._container.getStats(self.containerId)
            except NotFound:
                logging.info('Container %s not found: ' % self.containerId)
                break
            data_sample = {}
            for metric_map in self.getMetrics():
                data_sample[metric_map[0]+"."+metric_map[-1]] = self.getFromDict(
                                                                json_obj, metric_map)
            self.queue.put(data_sample)
            time.sleep(self.update_interval)
            if not jobid:
                command = ("docker exec %s ls -al | grep -m 1 'proc.' "
                           " | gawk 'BEGIN { FS = \".\" } ;{print $2}'"
                           % self.containerId)
                jobid = subprocess.check_output(command, shell=True)
                logging.info('Job correlation: %s_%s ' % (jobid[:-1], self.containerId))
        logging.info('Finalyzing docker stats container: %s ' % self.containerId)

    def run(self):
        self.getData()

    def getQueue(self):
        return self.queue

    def getFromDict(self, dataDict, mapList):
        return reduce(lambda d, k: d[k], mapList, dataDict)

    def stop(self):
        self.stoprequest.set()

    def getMetrics(self):
        metricNames = [
        ["precpu_stats", "system_cpu_usage"],
        ["precpu_stats", "cpu_usage", "total_usage"],
        ["precpu_stats", "cpu_usage", "usage_in_kernelmode"],
        ["precpu_stats", "cpu_usage", "usage_in_usermode"],
        ["networks", "eth0", "rx_dropped"],
        ["networks", "eth0", "rx_packets"],
        ["networks", "eth0", "tx_packets"],
        ["networks", "eth0", "tx_dropped"],
        ["networks", "eth0", "rx_bytes"],
        ["networks", "eth0", "rx_errors"],
        ["networks", "eth0", "tx_bytes"],
        ["networks", "eth0", "tx_errors"],
        ["memory_stats", "max_usage"],
        ["memory_stats", "usage"],
        ["memory_stats", "stats", "total_pgmajfault"],
        ["memory_stats", "stats", "inactive_file"],
        ["memory_stats", "stats", "pgpgin"],
        ["memory_stats", "stats", "total_writeback"],
        ["memory_stats", "stats", "pgmajfault"],
        ["memory_stats", "stats", "total_active_file"],
        ["memory_stats", "stats", "mapped_file"],
        ["memory_stats", "stats", "total_pgpgout"],
        ["memory_stats", "stats", "total_active_anon"],
        ["memory_stats", "stats", "total_pgfault"],
        ["memory_stats", "stats", "total_rss"],
        ["memory_stats", "stats", "writeback"],
        ["memory_stats", "stats", "total_pgpgin"],
        ["memory_stats", "stats", "inactive_anon"],
        ["memory_stats", "stats", "total_inactive_file"],
        ["memory_stats", "stats", "active_file"],
        ["memory_stats", "stats", "unevictable"],
        ["memory_stats", "stats", "total_mapped_file"],
        ["memory_stats", "stats", "active_anon"],
        ["memory_stats", "stats", "pgfault"],
        ["memory_stats", "stats", "total_cache"],
        ["memory_stats", "stats", "rss_huge"],
        ["memory_stats", "stats", "total_inactive_anon"],
        ["memory_stats", "stats", "pgpgout"],
        ["memory_stats", "stats", "total_unevictable"],
        ["memory_stats", "stats", "total_rss_huge"],
        ["memory_stats", "stats", "rss"],
        ["memory_stats", "stats", "cache"],
        ["memory_stats", "limit"],
        ["memory_stats", "failcnt"]
        ]
        return metricNames
