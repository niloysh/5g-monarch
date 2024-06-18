Dummy NFV Orchestrator
======================
This script provides a simple NFV (Network Function Virtualization) Orchestrator using Flask.
It uses the Kubernetes API to install and uninstall MDE and KPI Computation components.

Overview
--------
- Intended to be run on a Kubernetes control plane node to avoid loading kubeconfig.
- The monitoring manager component can make HTTP requests to this orchestrator to manage the lifecycle of MDE and KPI Computation components.
- Real NFV Orchestrators would have more complex logic and additional APIs.