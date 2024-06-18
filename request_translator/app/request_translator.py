# ----------------------------------------------------------------------------
# Author: Niloy Saha
# Email: niloysaha.ns@gmail.com
# version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Request translator component of Monarch.
"""

from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import shortuuid
import json
import requests
from app.kpi_manager import KPIManager
from app.service_orchestrator import ServiceOrchestratorManager
from app.db_manager import DatabaseManager
from app.comm_manager import CommunicationManager
from app.translation_manager import TranslationManager
from app.logger import setup_logger


class RequestTranslator:
    def __init__(self, monitoring_manager_uri, mongodb_uri, service_orchestrator_uri):
        self.app = Flask(__name__)
        self.logger = setup_logger("request_translator")
        self.monitoring_manager_uri = monitoring_manager_uri
        self.service_orchestrator_uri = service_orchestrator_uri
        self.mongodb_uri = mongodb_uri
        self.monitoring_requests = {}

        self.kpi_manager = KPIManager()
        self.service_orchestrator = ServiceOrchestratorManager(service_orchestrator_uri)
        self.database_manager = DatabaseManager(mongodb_uri)
        self.comm_manager = CommunicationManager(monitoring_manager_uri)
        self.translation_manager = TranslationManager(self.service_orchestrator)

        self._load_configuration()
        self._set_routes()

    def _load_configuration(self):
        with open("app/schema.json", "r") as file:
            self.schema = json.load(file)

    def _set_routes(self):
        self.app.add_url_rule(
            "/api/monitoring-requests",
            "submit_monitoring_request",
            self.submit_monitoring_request,
            methods=["POST"],
        )
        self.app.add_url_rule(
            "/api/monitoring-requests/<request_id>",
            "get_monitoring_request",
            self.get_monitoring_request,
            methods=["GET"],
        )
        self.app.add_url_rule(
            "/api/monitoring-requests",
            "get_all_monitoring_requests",
            self.get_all_monitoring_requests,
            methods=["GET"],
        )
        self.app.add_url_rule(
            "/api/supported-kpis",
            "get_supported_kpis",
            self.get_supported_kpis,
            methods=["GET"],
        )
        self.app.add_url_rule(
            "/api/monitoring-requests/delete/<request_id>",
            "delete_monitoring_request",
            self.delete_monitoring_request,
            methods=["DELETE"],
        )
        self.app.add_url_rule("/api/health", "health_check", self.health_check, methods=["GET"])

    def health_check(self):
        return jsonify({"status": "success", "message": "Request Translator is healthy"}), 200

    def submit_monitoring_request(self):
        data = request.get_json()
        try:
            validate(instance=data, schema=self.schema)
            if not self.kpi_manager.is_kpi_supported(data):
                return jsonify({"status": "error", "message": "KPI is not supported"}), 400

            request_id = shortuuid.uuid()  # Generate a unique request_id
            self.monitoring_requests[request_id] = data
            directive = self.translation_manager.translate_request(data, request_id)

            if self.comm_manager.send_directive(directive):
                return jsonify({"status": "success", "request_id": request_id}), 200
            else:
                self.monitoring_requests.pop(request_id)  # Remove the request if it fails to send to Monitoring Manager
                return jsonify({"status": "error", "message": "Failed to submit monitoring request"}), 500
        except ValidationError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    def get_monitoring_request(self, request_id):
        """
        Retrieve monitoring request by request_id
        """
        request_data = self.monitoring_requests.get(request_id)
        if request_data:
            return jsonify({"status": "success", "request_id": request_id, "data": request_data})
        else:
            return jsonify({"status": "error", "message": "Monitoring request not found"}), 404

    def get_all_monitoring_requests(self):
        # Return all monitoring requests
        return jsonify({"status": "success", "data": self.monitoring_requests})

    def get_supported_kpis(self):
        return jsonify({"status": "success", "supported_kpis": self.kpi_manager.list_supported_kpis()})

    def run(self, port):
        self.app.run(debug=True, port=port, host="0.0.0.0")

    def delete_monitoring_request(self, request_id):
        """
        Delete monitoring request by request_id
        """
        if request_id in self.monitoring_requests:
            request = self.monitoring_requests[request_id]
            kpi_name = request["kpi"]["kpi_name"]
            delete_directive = {"request_id": request_id, "action": "delete", "kpi_name": kpi_name}
            if self.comm_manager.send_delete_directive(delete_directive):
                del self.monitoring_requests[request_id]
                return jsonify({"status": "success", "message": "Monitoring request deleted"}), 200
            else:
                return jsonify({"status": "error", "message": "Failed to delete monitoring request"}), 500
        else:
            return jsonify({"status": "error", "message": "Monitoring request not found"}), 404
