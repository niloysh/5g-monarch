#!/bin/bash
kubectl get svc -n open5gs -l app=monarch -o json | jq .items[].metadata.name