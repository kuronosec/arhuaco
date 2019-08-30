#!/bin/bash

if [ "$1" == "dns" ]; then
    # normal
    cat $(find /var/lib/arhuaco/data/normal/ -name "dns.log" | sed ':a;N;$!ba;s/\n/ /g') \
    |   /opt/bro/bin/bro-cut query duration qclass qclass_name qtype qtype_name \
    |   grep -v "ubuntu\|192\.\|\-\s" > /var/lib/arhuaco/data/dns_normal.log
    # malicious
    cat /var/lib/arhuaco/data/malicious/network-sandbox/dns.log \
    |   /opt/bro/bin/bro-cut query duration qclass qclass_name qtype qtype_name \
    |   grep -v "ubuntu\|192\.\|\-\s" > /var/lib/arhuaco/data/dns_malicious.log
fi
