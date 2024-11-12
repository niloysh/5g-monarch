#!/bin/bash
NAMESPACE="monarch"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
kubectl delete --wait=true -f standard/kpi_calculator.yaml
