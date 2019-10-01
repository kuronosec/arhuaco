#!/bin/bash

cat /var/lib/arhuaco/data/normal_clean.csv | grep -v "signal" > /var/lib/arhuaco/data/normal_clean_filtered.csv
cat /var/lib/arhuaco/data/malicious_clean.csv | grep -v "signal" > /var/lib/arhuaco/data/malicious_clean_filtered.csv
