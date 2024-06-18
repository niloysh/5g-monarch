import json
import requests
import time
from app.logger import setup_logger


class ServiceOrchestratorManager:
    """
    Class that interacts with the Service Orchestrator to retrieve information about the slice components.
    """

    def __init__(self, service_orchestrator_uri):
        self.service_orchestrator_uri = service_orchestrator_uri
        self.logger = setup_logger("service_orchestrator")
        self.connect_to_service_orchestrator()

    def is_service_orchestrator_available(self):
        try:
            response = requests.get(self.service_orchestrator_uri + "/api/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def connect_to_service_orchestrator(self, max_retries=5, wait_time=5):
        attempt = 0
        while attempt < max_retries:
            self.logger.info(
                f"Attempt {attempt + 1} to connect to Service Orchestrator at {self.service_orchestrator_uri}"
            )
            if self.is_service_orchestrator_available():
                self.logger.info("Successfully connected to Service Orchestrator")
                return True
            attempt += 1
            time.sleep(wait_time)
        self.logger.error(f"Could not connect to Service Orchestrator after {max_retries} attempts")
        exit(1)

    def get_slice_components(self, slice_id, nsi=None):
        try:
            response = requests.get(self.service_orchestrator_uri + f"/slices/{slice_id}")
            if response.status_code == 200:
                self.logger.info(f"Successfully retrieved slice components for slice ID {slice_id}")
                pods = response.json()["pods"]
                return pods
            else:
                self.logger.error(f"Error retrieving slice components: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving slice components: {str(e)}")
            return None
