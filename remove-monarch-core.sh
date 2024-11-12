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
wait_for_pod_deletion() {
    local label_key=$1
    local label_value=$2
    echo "Waiting for pod with label $label_key=$label_value to be deleted in namespace $NAMESPACE..."

    while [ "$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" -o jsonpath='{.items[*].metadata.name}')" != "" ]; do
        sleep 5
        echo "Waiting for pod $label_value to be deleted..."
    done
    print_success "Pod $label_value is deleted."
}

# Set the namespace for Monarch
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"

print_header "Removing Data Store (Monarch Core [1/5])"
cd $WORKING_DIR/data_store
./uninstall.sh
wait_for_pod_deletion "app" "minio"
wait_for_pod_deletion "app.kubernetes.io/name" "mongodb"
print_success "Data store removed."

print_header "Removing Data Distribution (Monarch Core [2/5])"
cd $WORKING_DIR/data_distribution
./uninstall.sh
wait_for_pod_deletion "app.kubernetes.io/component" "storegateway"
wait_for_pod_deletion "app.kubernetes.io/component" "receive"
print_success "Data Distribution removed."

print_header "Removing Data Visualization (Monarch Core [3/5])"
cd $WORKING_DIR/data_visualization
./uninstall.sh
wait_for_pod_deletion "app.kubernetes.io/name" "grafana"
print_success "Data Visualization removed."

print_header "Removing Monitoring Manager (Monarch Core [4/5])"
cd $WORKING_DIR/monitoring_manager
./uninstall.sh
wait_for_pod_deletion "app.kubernetes.io/component" "monitoring-manager"
print_success "Monitoring manager removed."

print_header "Removing Request Translator (Monarch Core [5/5])"
cd $WORKING_DIR/request_translator
./uninstall.sh
wait_for_pod_deletion "component" "request-translator"
print_success "Request Translator removed."