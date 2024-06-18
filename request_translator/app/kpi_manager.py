import json
from app.logger import setup_logger


class KPIManager:
    def __init__(self):
        self.logger = setup_logger("kpi_manager")
        self.load_supported_kpis("app/supported_kpis.json")

    def load_supported_kpis(self, file_path):
        self.logger.info(f"Loading supported KPIs from {file_path}")
        with open(file_path, "r") as file:
            self.supported_kpis = json.load(file)

    def list_supported_kpis(self):
        return [
            {
                "kpi_name": kpi["kpi_name"],
                "kpi_description": kpi["kpi_description"],
                "kpi_unit": kpi["kpi_unit"],
            }
            for kpi in self.supported_kpis
        ]

    def is_kpi_supported(self, monitoring_request):
        kpi = monitoring_request.get("kpi")
        kpi_name = kpi.get("kpi_name")
        return any(kpi["kpi_name"] == kpi_name for kpi in self.supported_kpis)
