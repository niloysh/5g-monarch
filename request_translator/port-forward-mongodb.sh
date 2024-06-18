#!/bin/bash
## Forwarding the port of the MongoDB service to the local machine
## Needed for local development
kubectl port-forward service/datastore-mongodb -n monarch 27017:27017