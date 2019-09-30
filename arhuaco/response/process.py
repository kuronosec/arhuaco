import logging
import subprocess

from arhuaco.response.action import Action

class Process(Action):

    def __init__(self):
        self.configuration = None

    def execute_action(self, id):
        # kill malicious containers
        logging.info("Killing container with id: %s" % id)
        proc_log = subprocess.Popen("docker stop %s" % id,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
