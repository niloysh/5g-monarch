#!/bin/bash
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"

cd $WORKING_DIR/service_orchestrator
./test-service-orchestrator.sh

cd $WORKING_DIR/nfv_orchestrator
./test-nfv-orchestrator.sh