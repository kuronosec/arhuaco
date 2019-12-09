# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from arhuaco.analysis.arhuaco_model import ArhuacoModel
from arhuaco.response.arhuaco_response import ArhuacoResponse

from threading import Thread, Event
from queue import Queue, Empty

# This is the main class for data analysis in Arhuaco
class ArhuacoAnalysis:

    def __init__(self, input_queue_dict, output_queue):
        self.configuration    = None
        self.input_queue_dict = input_queue_dict
        self.output_queue     = output_queue
        self.model    = None

    def start_analysis(self):
        # docker_thread = Thread(target=worker)
        syscall_thread = Thread(target=self.start_stream_model,kwargs=dict(type="syscall"))
        network_thread = Thread(target=self.start_stream_model,kwargs=dict(type="network"))
        # docker_thread.start()
        syscall_thread.start()
        network_thread.start()

    def start_stream_model(self, type=None):
            self.model = ArhuacoModel(self.input_queue_dict,
                         self.output_queue)
            self.model.stream_analysis(type)

    def create_analysis_model(self, type):
            self.model = ArhuacoModel(None,None)
            self.model.initialize_model(type)
