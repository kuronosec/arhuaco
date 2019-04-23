# This example shows how ApMon can be used to send information about a given job 
# to the MonALISA service
import json
import re
import sys
import time
import threading
import apmon
from arhuaco.monitoring.utils.docker_utils import DockerUtils

class alien:

    def __init__(self, configurationPath):
        # Initialize ApMon specifying that it should not send information about the system.
        # Note that in this case the background monitoring process isn't stopped, in case you may
        # want later to monitor a job.
        self._configurationPath = configurationPath
        self._apm = apmon.ApMon(self._configurationPath)
        self._apm.setLogLevel("INFO")
        self._apm.confCheck = False
        self._apm.enableBgMonitoring(False)
        self._apm.setMaxMsgRate(1000)

    def sendData(self, id, data):
        # you can put as many pairs of parameter_name, 
        # parameter_value as you want
        # but be careful not to create packets longer than 8K.
        for key,value in data:
            self._apm.sendParameters("ALICE::UF::KUBERNETES_Jobs", id, { key:value } )
