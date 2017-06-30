#!/bin/bash

# Run Harness Project
cd /home/pleniter/Documents/tests/justin_test/
java -jar mpe-automate-jar-with-dependencies.jar

# Poll Server
sleep 30
curl -X POST '172.31.224.143:45000/Initiate' -d 'start planning'