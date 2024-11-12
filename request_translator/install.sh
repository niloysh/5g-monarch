#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="request-translator"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
KUSTOMIZATION_FILE="$SCRIPT_DIR/manifests/kustomization.yaml"
cd "$SCRIPT_DIR"
set -o allexport; source ../.env; set +o allexport

# Check if SERVICE_ORCHESTRATOR_URI is set
if [ -z "$SERVICE_ORCHESTRATOR_URI" ]; then
  echo "SERVICE_ORCHESTRATOR_URI is not set in the .env file"
  exit 1
fi

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE

kubectl create configmap slice-components-configmap --from-file=slice_components.json -n $NAMESPACE
envsubst < manifests/deployment.yaml | kubectl apply -f -
envsubst < manifests/service.yaml | kubectl apply -f -
