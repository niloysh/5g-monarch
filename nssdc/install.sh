#!/bin/bash
KUBE_PROMETHEUS_STACK_VER="51.9.4"
HELM_REPO_URL="https://prometheus-community.github.io/helm-charts"
HELM_REPO_NAME="prometheus-community"
NAMESPACE="monarch"

kubectl get namespace $NAMESPACE 2>/dev/null || kubectl create namespace $NAMESPACE
helm repo add $HELM_REPO_NAME $HELM_REPO_URL || echo "Helm repo $HELM_REPO_NAME already exists."
helm repo update

set -o allexport; source ../.env; set +o allexport
kubectl -n $NAMESPACE delete secret thanos-objstore-config --ignore-not-found
kubectl -n $NAMESPACE create secret generic thanos-objstore-config --from-file=thanos.yaml=<(envsubst < thanos-objstore-config.yaml)

kubectl -n $NAMESPACE delete secret additional-scrape-configs --ignore-not-found
kubectl -n $NAMESPACE create secret generic additional-scrape-configs --from-file=additional-scrape-configs.yaml=<(envsubst < additional-scrape-configs.yaml)

helm upgrade --install nssdc $HELM_REPO_NAME/kube-prometheus-stack \
        --namespace $NAMESPACE \
        --version $KUBE_PROMETHEUS_STACK_VER \
        --values <(envsubst < values.yaml)


