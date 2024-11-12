#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="monitoring-manager"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
set -o allexport; source ../.env; set +o allexport
kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
envsubst < manifests/deployment.yaml | kubectl delete -f -
envsubst < manifests/service.yaml | kubectl delete -f -
