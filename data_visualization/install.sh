#!/bin/bash
KUBE_PROMETHEUS_STACK_VER="51.9.4"
HELM_REPO_URL="https://prometheus-community.github.io/helm-charts"
HELM_REPO_NAME="prometheus-community"
NAMESPACE="monarch"
MODULE_NAME="dataviz"

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
helm repo add $HELM_REPO_NAME $HELM_REPO_URL || echo "Helm repo $HELM_REPO_NAME already exists."
helm repo update
set -o allexport; source ../.env; set +o allexport

helm upgrade --install $MODULE_NAME $HELM_REPO_NAME/kube-prometheus-stack \
        --namespace $NAMESPACE \
        --version $KUBE_PROMETHEUS_STACK_VER \
        --values <(envsubst < values.yaml)

kubectl apply -k .