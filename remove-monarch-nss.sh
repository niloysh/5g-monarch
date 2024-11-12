#!/bin/bash
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

print_header "Removing NSSDC (Monarch NSS [1/1])"
cd $WORKING_DIR/nssdc
./uninstall.sh
wait_for_pod_deletion "app.kubernetes.io/name" "prometheus"
print_success "NSSDC removed."