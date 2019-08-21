#!/bin/bash

# Extract the system calls made from the jobs in the containers
# for normal jobs
if [ "$1" == "normal" ]
then
    find ./iri* -type f -name "trace.scap*" -print0 | while IFS= read -r -d $'\0' line; do
        sysdig -r "$line" \
        -p'%container.id %thread.tid %evt.category %evt.type %evt.args' \
        evt.category!= sleep and evt.category!=wait and evt.category!=IPC \
        and evt.category!=ipc and evt.category!=scheduler and evt.category!=switch \
        and evt.category!=signal and evt.category!=unknown \
        and container.name contains alien | awk '{print>>"extracted/"$1"-"$2".log"}'
    done
elif [ "$1" == "malicious" ]
then
    # Do the same for malicious jobs
    find ./new_analysis_malicious -type f -name "sysdig.log" -print0 | while IFS= read -r -d $'\0' line; do
        cat "$line" | awk '{print>>"extracted/"$1"-"$2".log"}'
    done
fi
