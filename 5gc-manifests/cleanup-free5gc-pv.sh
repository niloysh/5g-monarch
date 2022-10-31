#!/bin/bash
kubectl delete pvc datadir-mongodb-0 -n test
kubectl delete pv free5gc-local-pv
