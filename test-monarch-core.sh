#!/bin/bash
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"

cd $WORKING_DIR/data_store
./test-data-store.sh

cd $WORKING_DIR/data_distribution
./test-data-distribution.sh

cd $WORKING_DIR/data_visualization
./test-data-visualization.sh

cd $WORKING_DIR/monitoring_manager
./test-monitoring-manager.sh

cd $WORKING_DIR/request_translator
./test-request-translator.sh