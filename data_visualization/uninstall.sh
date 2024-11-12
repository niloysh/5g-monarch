#!/bin/bash
CHART_VERSION="8.6.0"
HELM_REPO_URL="https://grafana.github.io/helm-charts"
HELM_REPO_NAME="grafana"
HELM_CHART_NAME="grafana"
NAMESPACE="monarch"
MODULE_NAME="dataviz"

helm uninstall $MODULE_NAME \
        --namespace $NAMESPACE \

kubectl delete -k .