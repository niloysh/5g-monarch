#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="kpi-computation"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
set -o allexport; source ../.env; set +o allexport
kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
envsubst < standard/kpi_calculator.yaml | kubectl apply -f -

print_success() {
    echo -e "\e[1;32m$1\e[0m"
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

wait_for_pod_ready "component" "kpi-calculator"