from flask import Flask, request, jsonify
import os
import logging
import subprocess
import json

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


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


class DummyNFVOrchestrator:
    def __init__(self):
        self.logger = setup_logger("nfv_orchestrator")
        self.logger.info("NFV Orchestrator started")
        self.app = Flask(__name__)

        self._set_routes()

    def _set_routes(self):
        self.app.add_url_rule("/mde/install", "mde_install", self.mde_install, methods=["POST"])
        self.app.add_url_rule("/mde/uninstall", "mde_uninstall", self.mde_uninstall, methods=["POST"])
        self.app.add_url_rule("/mde/check", "mde_check", self.mde_check, methods=["POST"])
        self.app.add_url_rule(
            "/kpi-computation/install", "kpi_computation_install", self.kpi_computation_install, methods=["POST"]
        )
        self.app.add_url_rule(
            "/kpi-computation/uninstall", "kpi_computation_uninstall", self.kpi_computation_uninstall, methods=["POST"]
        )
        self.app.add_url_rule(
            "/kpi-computation/check", "kpi_computation_check", self.kpi_computation_check, methods=["POST"]
        )
        self.app.add_url_rule("/api/health", "check_health", self.check_health, methods=["GET"])

    def mde_install(self):
        return_value = os.system(f"{WORKING_DIR}/../mde/install.sh")
        if return_value != 0:
            return jsonify({"status": "error", "message": "MDE installation failed"}), 500
        else:
            return jsonify({"status": "success", "message": "MDE installed"}), 200

    def mde_uninstall(self):
        return_value = os.system(f"{WORKING_DIR}/../mde/uninstall.sh")
        if return_value != 0:
            return jsonify({"status": "error", "message": "MDE uninstallation failed"}), 500
        else:
            return jsonify({"status": "success", "message": "MDE uninstalled"}), 200

    def mde_check(self):
        try:
            # Run the command and capture output
            result = subprocess.run(
                [f"{WORKING_DIR}/../mde/check-mde.sh"],
                capture_output=True,
                text=True,
                check=True
            )
            return jsonify({"status": "success", "message": "MDE test success", "output": result.stdout}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({"status": "error", "message": "MDE test failed", "output": e.stderr}), 500

    def kpi_computation_install(self):
        return_value = os.system(f"{WORKING_DIR}/../kpi_computation/install.sh")
        if return_value != 0:
            return jsonify({"status": "error", "message": "KPI Computation installation failed"}), 500
        else:
            return jsonify({"status": "success", "message": "KPI Computation installed"}), 200

    def kpi_computation_uninstall(self):
        return_value = os.system(f"{WORKING_DIR}/../kpi_computation/uninstall.sh")
        if return_value != 0:
            return jsonify({"status": "error", "message": "KPI Computation uninstallation failed"}), 500
        else:
            return jsonify({"status": "success", "message": "KPI Computation uninstalled"}), 200

    def kpi_computation_check(self):
        try:
            # Run the command and capture output
            result = subprocess.run(
                [f"{WORKING_DIR}/../kpi_computation/check-kpi.sh"],
                capture_output=True,
                text=True,
                check=True
            )
            return jsonify({"status": "success", "message": "KPI test success", "output": result.stdout}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({"status": "error", "message": "KPI test failed", "output": e.stderr}), 500

    def check_health(self):
        return jsonify({"status": "success", "message": "NFV Orchestrator is healthy"}), 200

    def run(self, debug, port, host):
        self.app.run(debug=debug, port=port, host=host)


if __name__ == "__main__":
    nfvo = DummyNFVOrchestrator()
    nfvo.run(debug=True, port=6001, host="0.0.0.0")
