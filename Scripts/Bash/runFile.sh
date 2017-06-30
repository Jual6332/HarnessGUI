#!/bin/bash

# Run Logger, PlanServer, Harness Code
gnome-terminal --tab -e 'bash -c /opt/pleniter/logger/pleniter-logger.sh;bash' --tab -e 'bash -c /opt/pleniter/plan/planServer/planServer.sh;bash' --tab -e 'bash -c /home/pleniter/Documents/tests/justin_test/Harness_VM_Testing/Scripts/Bash/runMore.sh;bash' --tab -e 'bash -c /home/pleniter/Documents/tests/justin_test/Harness_VM_Testing/Scripts/Bash/POST.sh;bash'