#!/sbin/sh

cat /home/data/normal_clean.csv | grep -v "signal" > /home/data/normal_clean_filtered.csv

