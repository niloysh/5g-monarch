#!/bin/bash
NAMESPACE="monarch"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
# kubectl delete -f standard/metrics-servicemonitor.yaml
kubectl delete -f metrics-service.yaml