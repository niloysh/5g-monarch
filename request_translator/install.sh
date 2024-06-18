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

# Replace placeholder in kustomization.yaml with the actual URI
sed -i "s|SERVICE_ORCHESTRATOR_URI=.*|SERVICE_ORCHESTRATOR_URI=$SERVICE_ORCHESTRATOR_URI|g" "$KUSTOMIZATION_FILE"

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
kubectl apply -k manifests/ -n monarch
