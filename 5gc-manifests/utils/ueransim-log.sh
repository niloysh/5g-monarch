#!/usr/bin/env bash

function_name=$1
container_name=$2
namespace="test"

echo "Function name: $function_name"
echo "Container name: $container_name"

if [[ -z $container_name ]]; then
    kubectl logs -f deployments/ueransim-$function_name -n $namespace
else
    kubectl logs -f deployments/ueransim-$function_name -c $container_name -n $namespace
fi

