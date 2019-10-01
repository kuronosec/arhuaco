# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import sys, time
import logging
import socket

from queue import Queue, Empty
from arhuaco.sensors.arhuaco_sensors import ArhuacoSensors
from arhuaco.analysis.arhuaco_analysis import ArhuacoAnalysis
from arhuaco.response.arhuaco_response import ArhuacoResponse

data_path = "/var/lib/arhuaco/data"
log_path  = "/var/log/arhuaco/"
log_file  = "%s/%s-arhuaco.log" % (log_path, socket.gethostname())
pid_file  = "/var/log/arhuaco/arhuaco.pid"

def run():
    logging.basicConfig(filename=log_file,
                        level=logging.INFO)
    # create the arhuaco services
    # First create a dictionary for storing
    # the queues that bring data from different
    # sources
    input_queue_dict = {}
    # for the time being we only have a queue with
    # outpur results
    output_queue = Queue()
    logging.info('Creating Arhuaco services...')
    arhuaco_sensors_service = ArhuacoSensors(input_queue_dict)
    arhuaco_analysis_service = ArhuacoAnalysis(input_queue_dict,
                                               output_queue)
    arhuaco_response_service = ArhuacoResponse(output_queue)
    # start the services
    logging.info('Starting the Arhuaco services...')
    arhuaco_sensors_service.start_sensors()
    arhuaco_analysis_service.start_analysis()
    arhuaco_response_service.start_response()
    logging.info('Arhuaco service started...')

if __name__ == "__main__":
    run()
