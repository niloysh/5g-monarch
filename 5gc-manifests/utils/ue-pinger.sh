#!/usr/bin/env bash

ue=$1
count=$2

if [[ -z $count ]]; then
   echo "Pinging continuously ..."
   kubectl exec -it -n test deployments/ueransim-$ue -- ping -I uesimtun0 www.google.ca 
else
   echo "Pinging $count times..."
   kubectl exec -it -n test deployments/ueransim-$ue -- ping -I uesimtun0 www.google.ca -c $count
fi
