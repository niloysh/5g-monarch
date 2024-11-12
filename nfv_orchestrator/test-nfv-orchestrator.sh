#!/bin/bash

print_subheader() {
    echo -e "\e[1;36m--- $1 ---\e[0m"
}

print_header() {
    echo -e "\n\e[1;34m############################### $1 ###############################\e[0m"
}

print_success() {
    echo -e "\e[1;32m$1\e[0m"
}

print_error() {
    echo -e "\e[1;31mERROR: $1\e[0m"
}

print_info() {
    echo -e "\e[1;33mINFO: $1\e[0m"
}

# Set namespace and endpoint
NAMESPACE="monarch"
HEALTH_ENDPOINT="http://localhost:6001/api/health"

# Check the health of the Monitoring Manager
print_header "Testing NFV Orchestrator (External Component [2/2])"
response=$(curl -s -w "%{http_code}" -o /dev/null $HEALTH_ENDPOINT)

if [ "$response" -eq 200 ]; then
    print_success "Health check passed! NFV Orchestrator is healthy."
else
    print_error "Health check failed with status code: $response. Please check the NFV Orchestrator logs for details."
    exit 1
fi

# Function to check if a pod with a specific label is ready
check_pod_ready() {
    local label_key=$1
    local label_value=$2
    print_subheader "Checking if pod $label_value exists and is ready"

    # Check if the pod with the given label exists
    POD_EXISTS=$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" --no-headers | wc -l)

    if [ "$POD_EXISTS" -eq 0 ]; then
        print_info "Pod with label $label_key=$label_value does not exist."
        return 2  # Indicate that the pod does not exist
    fi

    # Check if the pod is ready
    POD_READY=$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" -o jsonpath='{.items[0].status.containerStatuses[0].ready}')

    if [ "$POD_READY" == "true" ]; then
        print_success "Pod with label $label_key=$label_value is ready."
        return 0  # Pod is ready
    else
        print_error "Pod with label $label_key=$label_value is not ready."
        return 1  # Pod is not ready
    fi
}

# Check if the pod with the label 'app.kubernetes.io/name=prometheus' is ready
check_pod_ready "app.kubernetes.io/name" "prometheus"

# If the pod is ready, execute the curl commands; otherwise, skip them
if [ $? -eq 0 ]; then
    print_subheader "Pod is ready. Executing MDE and KPI tests using NFVO"
    curl -X POST http://localhost:6001/mde/check
    curl -X POST http://localhost:6001/kpi-computation/check
    print_success "MDE and KPI tests completed. If output is empty, then MDEs and KPI module(s) are not installed."
else
    print_info "NSSDC is not READY. Skipping MDE and KPI tests. Likely NSSDC is not yet deployed."
fi