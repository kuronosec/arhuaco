#!/bin/bash

if [ "$1" == "name" ]; then
    # For only single parameter
    # Extract normal data
    cat /var/lib/arhuaco/data/syscalls-* | gawk {'print $3'} > "$2/normal_name.csv"
    # Extract malicious data
    for F in `sudo find /var/lib/arhuaco/data/malicious/analyses/ -name "syscalls-*"`; do sudo cat $F | gawk {'print $3'} >> "$2/malicious_name.csv"; done
elif [ "$1" == "parameters" ]; then
        # For only single parameter
    # Extract normal data
    cat /var/lib/arhuaco/data/syscalls-* | gawk {'print $2, $3, $4'} > "$2/normal_parameters.csv"
    # Extract malicious data
    for F in `sudo find /var/lib/arhuaco/data/malicious/analyses/ -name "syscalls-*"`; do sudo cat $F | gawk {'print $2, $3, $4'} >> "$2/malicious_parameters.csv"; done
elif [ "$1" == "io" ]; then
    # For only single parameter
    # Extract normal data
    cat /var/lib/arhuaco/data/syscalls-* | grep " net \| file " | gawk {'print $2, $3, $4'} > "$2/normal_io.csv"
    # Extract malicious data
    for F in `sudo find /var/lib/arhuaco/data/malicious/analyses/ -name "syscalls-*"`; do sudo cat $F | grep " net \| file " | gawk {'print $2, $3, $4'} >> "$2/malicious_io.csv"; done
elif [ "$1" == "full" ]; then
    for file in $(find /var/lib/arhuaco/data/malicious/simulated_analyses/ -name "sysdig.log*" )
    do
        cat $file >> /var/lib/arhuaco/data/malicious/malicious.csv
    done
fi
