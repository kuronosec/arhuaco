# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import os
import sys, getopt
import numpy as np
import time
import logging
import socket

from flask import Flask
from flask import request,jsonify
from arhuaco.analysis.arhuaco_model import ArhuacoModel

from threading import Thread, Event
from queue import Queue, Empty

import tensorflow as tf

# Global model object for Flask
rest_model = None

# This is the main class for data analysis in Arhuaco

class ArhuacoAnalysis:

    def __init__(self, input_queue_dict, output_queue):
        self.configuration    = None
        self.input_queue_dict = input_queue_dict
        self.output_queue     = output_queue
        self.model    = None

    def start_analysis(self):
        # docker_thread = Thread(target=worker)
        self.start_analysis_model("REST")
        syscall_thread = Thread(target=self.start_analysis_model,kwargs=dict(type="syscall"))
        network_thread = Thread(target=self.start_analysis_model,kwargs=dict(type="network"))
        # docker_thread.start()
        syscall_thread.start()
        network_thread.start()

    def start_analysis_model(self, type=None):
        # Create objects
        global rest_model
        self.model = ArhuacoModel(self.input_queue_dict,
                                  self.output_queue)
        if type == "REST":
            self.model.initialize_model("network")
            rest_model = self.model
            self.start_rest_service()
        else:
            self.model.stream_analysis(type)

    def start_rest_service(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 4444))
        port = sock.getsockname()[1]
        sock.close()
        logging.info("Running web app.")
        app.run(threaded=True, host="0.0.0.0", port=port)


app = Flask(__name__)

@app.route("/apply", methods=['GET'])
def predict():
    src_ip = request.args.get('src')
    # src_port = request.args.get('srcport')
    dst_ip = request.args.get('dst')
    # dst_port = request.args.get('dstport')

    global rest_model
    logging.info(src_ip+" "+dst_ip)
    # result = rest_model.predict()
    r = {}
    r['is_malicious'] = "malicious"
    return jsonify(r)
