import requests
import time
from app.logger import setup_logger


class CommunicationManager:
    def __init__(self, monitoring_manager_uri):
        self.monitoring_manager_uri = monitoring_manager_uri
        self.logger = setup_logger("comm_manager")
        self.connect_to_monitoring_manager()

    def is_monitoring_manager_available(self):
        try:
            response = requests.get(self.monitoring_manager_uri + "/api/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def connect_to_monitoring_manager(self, max_retries=5, wait_time=5):
        attempt = 0
        while attempt < max_retries:
            self.logger.info(f"Attempt {attempt + 1} to connect to Monitoring Manager at {self.monitoring_manager_uri}")
            if self.is_monitoring_manager_available():
                self.logger.info("Successfully connected to Monitoring Manager")
                return True
            attempt += 1
            time.sleep(wait_time)
        self.logger.error(f"Could not connect to Monitoring Manager after {max_retries} attempts")
        exit(1)

    def send_directive(self, directive):
        """
        Send directive to Monitoring Manager
        """
        monitoring_manager_url = self.monitoring_manager_uri + "/api/monitoring-directives"
        try:
            response = requests.post(monitoring_manager_url, json=directive)
            if response.status_code == 200:
                self.logger.info(f"Directive sent successfully with status code {response.status_code}")
                return True
            else:
                self.logger.error(f"Failed to send directive: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error in sending directive to Monitoring Manager: {e}")
            return False

    def send_delete_directive(self, directive):
        """
        Send directive to Monitoring Manager to delete a monitoring request
        """
        monitoring_manager_url = self.monitoring_manager_uri + "/api/monitoring-directives/delete"
        try:
            response = requests.post(monitoring_manager_url, json=directive)
            if response.status_code == 200:
                self.logger.info(f"Delete directive sent successfully with status code {response.status_code}")
                return True
            else:
                self.logger.error(f"Failed to send delete directive: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error in sending delete directive to Monitoring Manager: {e}")
            return False
