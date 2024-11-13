#!/bin/bash

# Run kubectl get pods with JSON output and extract the IP of the control plane node
control_plane_ip=$(kubectl get nodes -o json | jq -r '.items[0].status.addresses[0].address')
echo $control_plane_ip