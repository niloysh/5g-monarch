#!/bin/bash
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"

cd $WORKING_DIR/nssdc
./test-nssdc.sh