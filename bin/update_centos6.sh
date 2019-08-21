#!/bin/bash

scp -r root@iri03:/home/andres/development/thesis-repository/AliEn ./AliEn

scp -r ./AliEn kurono@iri04:/home/kurono/test/AliEn
scp -r ./AliEn kurono@iri31:/home/kurono/test/AliEn
scp -r ./AliEn root@iri34:/home/kurono/test/AliEn
scp -r ./AliEn kurono@iri39:/home/kurono/test/AliEn

parallel-ssh -t 0 -i -h hosts "cd /home/kurono/test/AliEn/centos6/; docker build -t uf:centos6 ./"
