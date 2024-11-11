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

wait_for_pod_running() {
    local label_key=$1
    local label_value=$2
    echo "Waiting for pod with label $label_key=$label_value to be running in namespace $NAMESPACE..."

    # Check if the pod exists
    pod_count=$(kubectl get pods -n "$NAMESPACE" -l "$label_key=$label_value" --no-headers | wc -l)
    
    if [ "$pod_count" -eq 0 ]; then
        print_error "No pods found with label $label_key=$label_value in namespace $NAMESPACE."
        return 1
    fi

    # Wait for the pod to be in Running state
    while : ; do
        # Get the pod status
        pod_status=$(kubectl get pods -n "$NAMESPACE" -l "$label_key=$label_value" -o jsonpath='{.items[*].status.phase}')
        
        # Check if the pod is in 'Running' state
        if [[ "$pod_status" =~ "Running" ]]; then
            print_success "Pod $label_value is now running."
            break
        else
            echo "Pod $label_value is not running yet. Waiting..."
            sleep 5
        fi
    done
}

# Set the namespace for Monarch
NAMESPACE="monarch"
USER="$(whoami)"
WORKING_DIR="$(pwd)"


print_header "Deploying Data Store (Monarch Core [1/5])"
cd $WORKING_DIR/data_store
./install.sh
wait_for_pod_ready "app" "minio"
wait_for_pod_ready "app.kubernetes.io/name" "mongodb"
./install-mc.sh
print_success "Data Store deployed."

print_header "Deploying Data Distribution (Monarch Core [2/5])"
cd $WORKING_DIR/data_distribution
./install.sh
wait_for_pod_ready "app.kubernetes.io/component" "storegateway"
wait_for_pod_ready "app.kubernetes.io/component" "receive"
print_success "Data Distribution deployed."


print_header "Deploying Data Visualization (Monarch Core [3/5])"
cd $WORKING_DIR/data_visualization
./install.sh
wait_for_pod_ready "app.kubernetes.io/name" "grafana"
print_success "Data Visualization deployed."


print_header "Deploying Monitoring Manager (Monarch Core [4/5])"
cd $WORKING_DIR/monitoring_manager
./install.sh
wait_for_pod_ready "component" "monitoring-manager"
print_success "Monitoring manager deployed."

print_header "Deploying Request Translator (Monarch Core [5/5])"
cd $WORKING_DIR/request_translator
./install.sh
wait_for_pod_ready "component" "request-translator"
print_success "Request Translator deployed."