#!/bin/bash
NAMESPACE="monarch"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
set -o allexport; source ../.env; set +o allexport
kubectl apply -f metrics-service.yaml
# envsubst < standard/metrics-servicemonitor.yaml | kubectl apply -f -
