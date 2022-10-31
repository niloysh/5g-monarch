#!/bin/bash

wait_for_pods_removed(){
    CMD="kubectl get pods -n test | grep "$2" | grep Terminating | wc -l"
    NUMPODS=$(eval "$CMD")
    while [ $NUMPODS -gt 0 ]; do
        sleep 5
        NUMPODS=$(eval "$CMD")
        echo "> waiting for $NUMPODS/$1 $2 pods to terminate"
    done
}

kubectl delete -f ../ueransim-v3.2.6-ue-slice-x3/ --recursive -n test
wait_for_pods_removed 6 ueransim-ue

kubectl delete -f ../ueransim-v3.2.6-gnb/ --recursive -n test
wait_for_pods_removed 1 ueransim-gnb

kubectl delete -f ../free5gc-v3.2.0-slice-x3-mon/ --recursive -n test
wait_for_pods_removed 12 free5gc

echo "Uninstall finished."