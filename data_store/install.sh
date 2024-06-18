#!/bin/bash
MINIO_VERSION="5.0.15"
HELM_REPO_URL="https://charts.min.io/"
HELM_REPO_NAME="minio"
NAMESPACE="monarch"
MODULE_NAME="datastore"

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
helm repo add $HELM_REPO_NAME $HELM_REPO_URL || echo "Helm repo $HELM_REPO_NAME already exists."
helm repo update

helm upgrade --install $MODULE_NAME $HELM_REPO_NAME/minio \
        --namespace $NAMESPACE \
        --version $MINIO_VERSION \
        --values minio/values.yaml

kubectl apply -k mongodb/ -n $NAMESPACE