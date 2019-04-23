import sys
import time
from threading import Thread
import arhuaco.monitoring.source.docker_metrics
import arhuaco.monitoring.source.sysdig_metrics
import prometheus
from queue import Queue, Empty

def main(argv):
    # Create variables
    docker_metrics_variable = docker_metrics.docker_metrics('unix://var/run/docker.sock',
                                                        '12104c0a5f66', 30)
    sysdig_metrics_variable = sysdig_metrics.sysdig_metrics('12104c0a5f66')
    backend = prometheus.prometheus('12104c0a5f66', 8000, queue=None)
    # get data queues
    queue_docker = docker_metrics_variable.getQueue()
    queue_sysdig = sysdig_metrics_variable.getQueue()    
    # Start Theads
    Thread(target=docker_metrics_variable.getData, name='docker_metrics_variable.getData').start()
    Thread(target=sysdig_metrics_variable.getData, name='sysdig_metrics_variable.getData').start()
    Thread(target=backend.write, name='backend.write.pull',
                 args=[queue_docker, 'pull']).start()
    Thread(target=backend.write, name='backend.write.push', 
                 args=[queue_sysdig, 'push']).start()

if __name__ == "__main__":
   main(sys.argv[1:])
