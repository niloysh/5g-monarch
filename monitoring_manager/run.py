from app.monitoring_manager import MonitoringManager
from app.logger import setup_logger
import os
from dotenv import load_dotenv

load_dotenv()
NFV_ORCHESTRATOR_URI = os.getenv("NFV_ORCHESTRATOR_URI", "http://localhost:6001")


def main():
    logger = setup_logger("app")
    logger.info("Starting Monitoring Manager service")

    monitoring_manager = MonitoringManager(NFV_ORCHESTRATOR_URI)
    monitoring_manager.run(debug=True, port=6000, host="0.0.0.0")


if __name__ == "__main__":
    main()
