import requests
import time
from app.logger import setup_logger


class NFVOrchestratorManager:
    def __init__(self, nfv_orchestrator_uri):
        self.logger = setup_logger("nfv_orchestrator")
        self.nfv_orchestrator_uri = nfv_orchestrator_uri
        self.connect_to_nfv_orchestrator()

    def is_nfv_orchestrator_available(self):
        try:
            response = requests.get(self.nfv_orchestrator_uri + "/api/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def connect_to_nfv_orchestrator(self, max_retries=5, wait_time=5):
        attempt = 0
        while attempt < max_retries:
            self.logger.info(f"Attempt {attempt + 1} to connect to NFV Orchestrator at {self.nfv_orchestrator_uri}")
            if self.is_nfv_orchestrator_available():
                self.logger.info("Successfully connected to NFV Orchestrator")
                return True
            attempt += 1
            time.sleep(wait_time)
        self.logger.error(f"Could not connect to NFV Orchestrator after {max_retries} attempts")
        exit(1)

    def mde_install(self):
        response = requests.post(self.nfv_orchestrator_uri + "/mde/install")
        return response

    def mde_uninstall(self):
        response = requests.post(self.nfv_orchestrator_uri + "/mde/uninstall")
        return response

    def kpi_computation_install(self):
        response = requests.post(self.nfv_orchestrator_uri + "/kpi-computation/install")
        return response

    def kpi_computation_uninstall(self):
        response = requests.post(self.nfv_orchestrator_uri + "/kpi-computation/uninstall")
        return response
