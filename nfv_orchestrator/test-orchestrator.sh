#!/bin/bash
curl -X GET http://localhost:6001/api/health
# curl -X POST http://localhost:6001/mde/uninstall
curl -X POST http://localhost:6001/mde/install
curl -X POST http://localhost:6001/kpi-computation/install