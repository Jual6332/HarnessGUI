#!/bin/bash

# Poll Server
sleep 40
curl -X POST '172.31.224.143:45000/Initiate' -d 'start planning'