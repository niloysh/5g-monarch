#!/bin/bash
THANOS_VER="12.4.3"
HELM_REPO_URL="https://charts.bitnami.com/bitnami"
HELM_REPO_NAME="bitnami"
NAMESPACE="monarch"
MODULE_NAME="datadist"

set -o allexport; source ../.env; set +o allexport

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
helm repo add $HELM_REPO_NAME $HELM_REPO_URL || echo "Helm repo $HELM_REPO_NAME already exists."
helm repo update


envsubst < thanos-values.yaml | helm upgrade --install $MODULE_NAME $HELM_REPO_NAME/thanos \
        --namespace $NAMESPACE \
        --version $THANOS_VER \
        -f -