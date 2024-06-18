#!/bin/bash
KUBE_PROMETHEUS_STACK_VER="51.9.4"
HELM_REPO_URL="https://prometheus-community.github.io/helm-charts"
HELM_REPO_NAME="prometheus-community"
NAMESPACE="monarch"
MODULE_NAME="datadist"

helm uninstall $MODULE_NAME \
        --namespace $NAMESPACE \