#!/bin/bash

wait_for_pods_running(){
    CMD="kubectl get pods -n test | grep free5gc | grep Running | wc -l"
    NUMPODS=$(eval "$CMD")
    while [ $NUMPODS -lt $1 ]; do
        sleep 5
        NUMPODS=$(eval "$CMD")
        echo "> waiting for $NUMPODS/$1 $2 pods"
    done
}


kubectl apply -f ../free5gc-v3.2.0-slice-x3-mon/ --recursive -n test

wait_for_pods_running 12 free5gc

kubectl apply -f ../ueransim-v3.2.6-gnb/ --recursive -n test

wait_for_pods_running 1 ueransim-gnb

kubectl apply -f ../ueransim-v3.2.6-ue-slice-x3/ --recursive -n test

wait_for_pods_running 6 ueransim-ue

echo "Install finished."