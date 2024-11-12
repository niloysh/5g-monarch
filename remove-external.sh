#!/bin/bash

# Function to print in color
print_header() {
    echo -e "\n\e[1;34m############################### $1 ###############################\e[0m"
}

print_success() {
    echo -e "\e[1;32m$1\e[0m"
}

print_error() {
    echo -e "\e[1;31mERROR: $1\e[0m"
}

NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"

# Check if the namespace exists
print_header "Checking if namespace '$NAMESPACE' exists"
kubectl get namespace $NAMESPACE 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Namespace '$NAMESPACE' not found. Exiting removal process."
    exit 1
fi


print_header "Deleting Monarch external components (i.e., Service Orchestrator and NFV Orchestrator)"
cd $WORKING_DIR/service_orchestrator
./uninstall.sh


cd $WORKING_DIR/nfv_orchestrator
./uninstall.sh

print_success "External components removed."