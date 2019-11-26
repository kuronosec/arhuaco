#!/bin/bash

# It starts and stops the container where arhuaco can also
# be executed.

if [ "$1" == "start" ]
then
    echo "Starting Arhuaco..."
    sudo docker run --name parsec-arhuaco -it -d \
                    -v /var/lib/arhuaco/data:/var/lib/arhuaco/data \
                    -v /var/log/arhuaco:/var/log/arhuaco \
                    -v /var/log/bro/current:/var/log/bro/current \
                    arhuaco /bin/bash
elif [ "$1" == "stop" ]
then
    echo "Stoping Arhuaco..."
    sudo docker stop parsec-arhuaco
else
    echo "Usage: arhuaco_container_ctl.sh <start/stop>"
fi
