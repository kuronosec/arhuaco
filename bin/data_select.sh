#!/bin/bash

# Extract the system calls made from the jobs in the containers
# for normal jobs
if [ "$1" == "normal" ]
then
    ls ./extracted |sort -R |tail -50000 |while read file; do
        cat ./extracted/$file >> new_normal.csv
    done
    cut -d' ' -f3- new_normal.csv > new_normal_ready.csv
# Do the same for the malicious data
elif [ "$1" == "malicious" ]
then
    find ./extracted/ -type f -name "*.log" -exec cat {} + >> new_malicious.csv
    cut -d' ' -f3- new_malicious.csv > new_malicious_ready.csv
fi
