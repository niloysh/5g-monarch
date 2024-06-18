import os
import argparse
from app.request_translator import RequestTranslator
from app.logger import setup_logger
from dotenv import load_dotenv

load_dotenv()
MONITORING_MANAGER_URI = os.getenv("MONITORING_MANAGER_URI", "http://localhost:6000")
SERVICE_ORCHESTRATOR_URI = os.getenv("SERVICE_ORCHESTRATOR_URI", "http://localhost:5001")
REQUEST_TRANSLATOR_PORT = int(os.getenv("REQUEST_TRANSLATOR_PORT", 7000))
MONARCH_MONGO_URI = os.getenv("MONARCH_MONGO_URI", "mongodb://localhost:27017/")
DEFAULT_SLICE_COMPONENTS_FILE = "app/slice_components.json"


def main():
    logger = setup_logger("app")
    logger.info("Starting RequestTranslator service")
    logger.info(f"Monitoring Manager URI: {MONITORING_MANAGER_URI}")
    logger.info(f"Monarch MongoDB URI: {MONARCH_MONGO_URI}")
    logger.info(f"Service Orchestrator URI: {SERVICE_ORCHESTRATOR_URI}")

    app = RequestTranslator(MONITORING_MANAGER_URI, MONARCH_MONGO_URI, SERVICE_ORCHESTRATOR_URI)
    app.run(port=REQUEST_TRANSLATOR_PORT)


if __name__ == "__main__":
    main()
