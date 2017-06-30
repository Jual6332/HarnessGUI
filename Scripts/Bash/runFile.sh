#!/bin/bash

# Run Logger
cd /opt/pleniter/logger
gnome-terminal -x ./pleniter-logger.sh 

# Run PlanServer
cd /opt/pleniter/plan/planServer
gnome-terminal -x ./planServer.sh

# Run Harness Code
cd /home/pleniter/Documents/tests/justin_test/Harness_VM_Testing/Scripts/Bash
gnome-terminal -x ./runMore.sh