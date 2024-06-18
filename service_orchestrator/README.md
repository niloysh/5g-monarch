Dummy Service Orchestrator
======================
This script provides a simple Service Orchestrator using Flask.
It uses the Kubernetes API to get information about the NFs.

Overview
--------
- Intended to be run on a Kubernetes control plane node to avoid loading kubeconfig.
- The monitoring manager component can make HTTP requests to this orchestrator to get infomation on slice components.
- Real service Orchestrators (e.g., ONAP) will have more complex logic and additional APIs.