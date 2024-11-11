#!/bin/bash
NAMESPACE="monarch"

 curl -X GET http://localhost:6001/api/health

check_pod_ready() {
    local label_key=$1
    local label_value=$2
    echo "Checking if pod with label $label_key=$label_value exists and is ready in namespace $NAMESPACE..."

    # Check if the pod with the given label exists
    POD_EXISTS=$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" --no-headers | wc -l)

    if [ "$POD_EXISTS" -eq 0 ]; then
        echo "Pod with label $label_key=$label_value does not exist."
        return 2  # Indicate that the pod does not exist
    fi

    # Check if the pod is ready
    POD_READY=$(kubectl get pods -n "$NAMESPACE" -l="$label_key=$label_value" -o jsonpath='{.items[0].status.containerStatuses[0].ready}')

    if [ "$POD_READY" == "true" ]; then
        echo "Pod with label $label_key=$label_value is ready."
        return 0  # Pod is ready
    else
        echo "Pod with label $label_key=$label_value is not ready."
        return 1  # Pod is not ready
    fi
}

# Check if the pod with the label 'app.kubernetes.io/name=prometheus' is ready
check_pod_ready "app.kubernetes.io/name" "prometheus"

# If the pod is not ready, skip the next curl commands
if [ $? -eq 0 ]; then
    # Pod is ready, execute the curl commands
    curl -X POST http://localhost:6001/mde/install
    curl -X POST http://localhost:6001/kpi-computation/install
else
    # Pod is not ready, skip the curl commands
    echo "NSSDC is not READY. Skipping MDE and KPI tests."
fi