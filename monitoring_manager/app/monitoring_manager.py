from app.logger import setup_logger
from app.orchestrator import NFVOrchestratorManager
from app.directive_manager import DirectiveManager
from flask import Flask, request, jsonify


class MonitoringManager:
    def __init__(self, nfv_orchestrator_uri):
        self.logger = setup_logger("monitoring_manager")
        self.app = Flask(__name__)
        self.directives = []
        self.nfv_orchestrator = NFVOrchestratorManager(nfv_orchestrator_uri)
        self.directive_manager = DirectiveManager(self.nfv_orchestrator)
        self._set_routes()

    def _set_routes(self):
        self.app.add_url_rule(
            "/api/monitoring-directives",
            "receive_directive",
            self.receive_directive,
            methods=["POST"],
        )
        self.app.add_url_rule(
            "/api/monitoring-directives/delete",
            "delete_directive",
            self.delete_directive,
            methods=["POST"],
        )
        self.app.add_url_rule(
            "/api/monitoring-directives",
            "list_directives",
            self.list_directives,
            methods=["GET"],
        )
        self.app.add_url_rule(
            "/api/health",
            "health_check",
            self.health_check,
            methods=["GET"],
        )

    def receive_directive(self):
        data = request.get_json()
        self.logger.info("Received directive: %s", data)
        self.directives.append(data)
        response = self.directive_manager.process_directive(data)
        return jsonify({"status": "success", "message": response.text}), response.status_code

    def health_check(self):
        return jsonify({"status": "success", "message": "Monitoring Manager is healthy"}), 200

    def delete_directive(self):
        data = request.get_json()
        self.logger.info("Received delete directive: %s", data)
        for directive in self.directives:
            if directive["request_id"] == data["request_id"]:
                self.directives.remove(directive)
                response = self.directive_manager.process_directive(data)
                return jsonify({"status": "success", "message": response.text}), response.status_code
        return jsonify({"status": "error", "message": "Directive not found"}), 404

    def list_directives(self):
        return jsonify(self.directives), 200

    def run(self, debug=False, port=5000, host="0.0.0.0"):
        self.app.run(debug=debug, port=port, host=host)
