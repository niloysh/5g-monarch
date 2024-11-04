# ----------------------------------------------------------------------------
# Author: Niloy Saha
# Email: niloysaha.ns@gmail.com
# version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Dummy Service Orchestrator
======================
This script provides a simple Service Orchestrator using Flask.
It uses the Kubernetes API to get information about the NFs.

Overview
--------
- Intended to be run on a Kubernetes control plane node to avoid loading kubeconfig.
- The monitoring manager component can make HTTP requests to this orchestrator to get infomation on slice components.
- Real service Orchestrators (e.g., ONAP) will have more complex logic and additional APIs.
"""
from flask import Flask, request, jsonify
import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


class DummyServiceOrchestrator:
    def __init__(self):
        self.logger = setup_logger("service_orchestrator")
        self.logger.info("Service Orchestrator started")
        self.app = Flask(__name__)
        self.slice_info = self._load_slice_info("slice_info.json")
        self._set_routes()

        # Kubernetes API server and token path
        self.api_server = "https://kubernetes.default.svc"
        self.token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        self.ca_cert_path = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

    def _set_routes(self):
        self.app.add_url_rule("/slices/<slice_id>", "get_slice_components", self.get_slice_components, methods=["GET"])
        self.app.add_url_rule("/api/health", "check_health", self.check_health, methods=["GET"])

    def get_slice_components(self, slice_id):
        if slice_id not in self.slice_info:
            self.logger.error(f"Slice ID {slice_id} not found in slice info.")
            return jsonify({"status": "error", "message": f"Slice ID {slice_id} not found"}), 404

        try:
            pods_info = self._get_pods_info()
            filtered_pods = self._filter_pods_by_slice_info(pods_info, self.slice_info[slice_id])
            filtered_pods = self._filter_response({"pods": filtered_pods})
            return jsonify({"status": "success", "pods": filtered_pods}), 200
        except Exception as e:
            self.logger.error(f"Error retrieving slice components: {str(e)}")
            return jsonify({"status": "error", "message": "Failed to retrieve slice components"}), 500

    def _get_pods_info(self):
        # Load the Kubernetes service account token
        with open(self.token_path, "r") as file:
            token = file.read().strip()

        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.api_server}/api/v1/namespaces/open5gs/pods"

        # Make an API request to the Kubernetes API server
        response = requests.get(url, headers=headers, verify=self.ca_cert_path)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to get pods: {response.status_code} - {response.text}")

        pods_info = response.json()
        return pods_info

    def _filter_response(self, response):
        filtered_response = []
        pods = response.get("pods", [])
        for pod in pods:
            pod_info = {}
            metadata = pod.get("metadata", {})
            name = metadata.get("name", "")
            nf = metadata.get("labels", {}).get("nf", "")
            pod_ip = pod.get("status", {}).get("podIP", "")

            pod_info["name"] = name
            pod_info["pod_ip"] = pod_ip
            pod_info["nss"] = "edge"
            pod_info["nf"] = nf
            filtered_response.append(pod_info)

        return filtered_response

    def _filter_pods_by_slice_info(self, pods_info, slice_pod_map):
        filtered_pods = []
        for pod in pods_info["items"]:
            pod_labels = pod.get("metadata", {}).get("labels", {})
            print(pod_labels)
            for item in slice_pod_map:
                name = item.get("nf")
                if name and pod_labels.get("name") == name:
                    filtered_pods.append(pod)
                    break

        self.logger.info(f"Filtered pods: {filtered_pods}")
        return filtered_pods

    def _load_slice_info(self, file_path):
        with open(file_path, "r") as file:
            slice_info = json.load(file)
            self.logger.info(f"Slice info loaded: {slice_info}")
        return slice_info

    def check_health(self):
        return jsonify({"status": "success", "message": "Service Orchestrator is healthy"}), 200

    def run(self, debug=False, port=5001, host="0.0.0.0"):
        self.app.run(debug=debug, port=port, host=host)


if __name__ == "__main__":
    service_orchestrator = DummyServiceOrchestrator()
    service_orchestrator.run(debug=True, port=5001, host="0.0.0.0")
