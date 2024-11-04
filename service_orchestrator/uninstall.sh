#!/bin/bash
NAMESPACE="monarch"
MODULE_NAME="service-orchestrator"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
kubectl delete -k .
