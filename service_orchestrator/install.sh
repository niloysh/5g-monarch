#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="service-orchestrator"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
set -o allexport; source ../.env; set +o allexport
kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
kubectl apply -k .
