# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

# Class with docker specific utilities
import re
from docker import Client

class DockerUtils:

    def __init__(self, socketPath):
        self._cli = Client(base_url=socketPath, version='auto')

    def getStats(self, containerName):
        stats_obj = self._cli.stats(containerName, False, False)
        return stats_obj

    def getInfo(self, containerId):
        info_obj = self._cli.inspect_container(container=containerId)
        return info_obj

    def getEvents(self, filters):
        events_obj = self._cli.events(filters= filters, decode=True)
        return events_obj

    def getLogs(self, containerName, streamLog):
        log_string = self._cli.logs(container = containerName, stream = streamLog)
        return log_string

    def getRegexpFromLogs(self, log_string, regularExpression, group):
        match = re.search(r""+regularExpression, log_string, re.MULTILINE)
        if match:
            return match.group(group)
        else:
            return None
