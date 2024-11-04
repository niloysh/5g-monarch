#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="monitoring-manager"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
set -o allexport; source ../.env; set +o allexport
kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE

# Check if NFV_ORCHESTRATOR_URI is set
if [ -z "$NFV_ORCHESTRATOR_URI" ]; then
    echo "Error: NFV_ORCHESTRATOR_URI is not set in .env file."
    exit 1
fi

sed -i.bak "s|NFV_ORCHESTRATOR_URI=http://<node_ip>:6001|NFV_ORCHESTRATOR_URI=${NFV_ORCHESTRATOR_URI}|g" manifests/kustomization.yaml && rm manifests/kustomization.yaml.bak

kubectl apply -k manifests/ -n monarch
