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


# Function to wait for a pod to be ready based on its label
wait_for_pod_ready() {
    local label_key=$1
    local label_value=$2
    echo "Waiting for pod with label $label_key=$label_value to be ready in namespace $NAMESPACE..."

    while [ "$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
        sleep 5
        echo "Waiting for pod $label_value to be ready..."
    done
    print_success "Pod $label_value is ready."
}

# Set the namespace for Monarch
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"


# Check if the namespace exists and create it if not
print_header "Checking if namespace '$NAMESPACE' exists"
kubectl get namespace $NAMESPACE 2>/dev/null || {
    print_error "Namespace '$NAMESPACE' not found. Creating it now..."
    kubectl create namespace $NAMESPACE
    print_success "Namespace '$NAMESPACE' created."
}


print_header "Installing Python dependencies"
pip3 install -r requirements.txt
print_success "Python dependencies installed."


print_header "Deploying Monarch external components (i.e., Service Orchestrator and NFV Orchestrator)"
cd $WORKING_DIR/service_orchestrator
./install.sh

cd $WORKING_DIR/nfv_orchestrator
./install.sh

print_success "External components deployed."