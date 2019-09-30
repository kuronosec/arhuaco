import sys
import time
import threading
import logging

from threading import Thread, Event
from arhuaco.response.action import Action
from arhuaco.response.message import Message
from arhuaco.response.process import Process

class ArhuacoResponse:

    def __init__(self, output_queue):
        self.configuration = self.analyze_config_file()
        self.output_queue  = output_queue

    def start_response(self):
        response_thread = Thread(target=self.process_result)
        response_thread.daemon = True
        response_thread.start()
        self.output_queue.join()

    def analyze_config_file(self):
        return None

    def process_result(self):
        while True:
            result = self.output_queue.get()
            self.process_result_analysis(result)
            self.output_queue.task_done()

    def process_result_analysis(self, result):
        send_message = Message()
        stop_process = Process()
        if result["value"][0] > 0.95:
           print("Intrusion detected!!!: result %s" % result)
           send_message.execute_action("Attacking sequence found in container %s, the following is the sequence: %s"
                                        % (result["id"],result["original"]))
           stop_process.execute_action(result["id"])
