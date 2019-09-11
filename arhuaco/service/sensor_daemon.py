import sys, time
import logging
import socket

from daemon import Daemon
from queue import Queue, Empty
from arhuaco.sensors.arhuaco_sensors import ArhuacoSensors

# TODO: this should be configured by files
data_path = "/var/lib/arhuaco/data"
log_path  = "/var/log/arhuaco/"
log_file  = "%s/%s-arhuaco-sensor.log" % (log_path, socket.gethostname())
pid_file  = "/var/lib/arhuaco/arhuaco-sensor.pid"

class SensorDaemon(Daemon):

    def run(self):
        logging.basicConfig(filename=log_file,
                            level=logging.INFO)
        logging.info('Creating Arhuaco client services...')
        arhuaco_sensors_service = ArhuacoSensors(None)
        # Start the services.
        logging.info('Starting the Arhuaco client services...')
        arhuaco_sensors_service.start_sensors()
        logging.info('Arhuaco service client started...')

    def stop(self):
        # TODO: do something here?
        logging.info('Service Arhuaco stopped ...')

if __name__ == "__main__":
    daemon = SensorDaemon( pid_file,
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
