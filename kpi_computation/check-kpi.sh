#!/bin/bash
kubectl get pods -n monarch -l app=monarch,component=kpi-calculator -o json | jq .items[].metadata.name