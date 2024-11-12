#!/bin/bash
CHART_VERSION="8.6.0"
HELM_REPO_URL="https://grafana.github.io/helm-charts"
HELM_REPO_NAME="grafana"
HELM_CHART_NAME="grafana"
NAMESPACE="monarch"
MODULE_NAME="dataviz"

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
helm repo add $HELM_REPO_NAME $HELM_REPO_URL || echo "Helm repo $HELM_REPO_NAME already exists."
helm repo update
set -o allexport; source ../.env; set +o allexport

helm upgrade --install $MODULE_NAME $HELM_REPO_NAME/grafana \
        --namespace $NAMESPACE \
        --version $CHART_VERSION \
        --values <(envsubst < values.yaml)

kubectl apply -k .