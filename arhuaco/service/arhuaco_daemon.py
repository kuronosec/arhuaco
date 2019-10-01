# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import sys, time
import logging
import socket

from daemon import Daemon
from queue import Queue, Empty
from arhuaco.sensors.arhuaco_input import ArhuacoInput
from arhuaco.analysis.arhuaco_analysis import ArhuacoAnalysis
from arhuaco.response.arhuaco_response import ArhuacoResponse

# TODO: this should be configured by files
data_path = "/var/lib/arhuaco/data"
log_path  = "/var/log/arhuaco/"
log_file  = "%s/%s-arhuaco-service.log" % (log_path, socket.gethostname())
pid_file  = "/var/lib/arhuaco/arhuaco-service.pid"

class ArhuacoDaemon(Daemon):

    def run(self):
        logging.basicConfig(filename=log_file,
                            level=logging.INFO)
        # It creates the Arhuaco services.
        # First create a dictionary for storing
        # the queues that bring data from different
        # sources.
        input_queue_dict = {}
        # For the time being we only have one queue with
        # output results.
        output_queue = Queue()
        logging.info('Creating Arhuaco services...')
        arhuaco_input_service = ArhuacoInput(input_queue_dict)
        arhuaco_analysis_service = ArhuacoAnalysis(input_queue_dict,
                                                   output_queue)
        arhuaco_response_service = ArhuacoResponse(output_queue)
        # Start the services.
        logging.info('Starting the Arhuaco services...')
        arhuaco_input_service.start_collecting_from_input()
        arhuaco_analysis_service.start_analysis()
        arhuaco_response_service.start_response()
        logging.info('Arhuaco service started...')

    def stop(self):
        # TODO: do something here?
        logging.info('Service Arhuaco stopped ...')

if __name__ == "__main__":
    daemon = ArhuacoDaemon( pid_file,
                            stdout=log_file,
                            stderr=log_file)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
