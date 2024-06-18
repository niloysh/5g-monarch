import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
from src.config import QUERIES, SCENARIOS
from dotenv import load_dotenv
load_dotenv()
import os

# Setup logger for console output
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(filename)s] %(message)s')
logger = logging.getLogger(__name__)

class PrometheusQuerier:
    def __init__(self, prometheus_url, local_timezone='America/Toronto'):
        self.prometheus_url = prometheus_url
        self.local_timezone = local_timezone
        self.query_endpoint = f"{prometheus_url}/api/v1/query_range"

    def get_time_range(self, start_time_str=None, end_time_str=None):
        if start_time_str and end_time_str:
            start_time = self.convert_local_to_utc(start_time_str)
            end_time = self.convert_local_to_utc(end_time_str)
        else:
            utc_now = datetime.utcnow()
            end_time = utc_now.strftime('%Y-%m-%dT%H:%M:%SZ')
            start_time = (utc_now - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
        return start_time, end_time
    
    @staticmethod
    def convert_local_to_utc(local_time_str, local_timezone='America/Toronto', output_format='%Y-%m-%dT%H:%M:%SZ'):
        local_time = datetime.strptime(local_time_str, '%Y-%m-%d %H:%M:%S')
        local_timezone_obj = pytz.timezone(local_timezone)
        local_time = local_timezone_obj.localize(local_time)
        utc_time = local_time.astimezone(pytz.utc)
        return utc_time.strftime(output_format)
    
    def query_prometheus(self, query_string, start_time_str=None, end_time_str=None, chunk_size_hours=1):
        # Initialize result dataframe
        df_result = pd.DataFrame(columns=["timestamp", "value"])

        start_time, end_time = self.get_time_range(start_time_str, end_time_str)
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
        chunk_size_seconds = chunk_size_hours * 3600
        
        while start_time < end_time:
            chunk_end_time = min(start_time + timedelta(seconds=chunk_size_seconds), end_time)
            data = {
                'query': query_string,
                'start': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'end': chunk_end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'step': '1s'
            }
            response = requests.post(url=self.query_endpoint, data=data, verify=False).json()
            df_chunk = self.extract_values(response)
            df_result = pd.concat([df_result, df_chunk], ignore_index=True)
            start_time += timedelta(seconds=chunk_size_seconds)
        
        df_result["value"] = pd.to_numeric(df_result["value"])
        return df_result
    
    @staticmethod
    def extract_values(prometheus_response):
        if prometheus_response["status"] == "error":
            logger.error("Error in Prometheus response!")
            return pd.DataFrame(columns=["timestamp", "value"])
        else:
            if not prometheus_response["data"]["result"]:
                logger.warning("Empty result in Prometheus response!")
                return pd.DataFrame(columns=["timestamp", "value"])
            result = prometheus_response["data"]["result"][0]["values"]
            return pd.DataFrame(result, columns=["timestamp", "value"])

def main():
    prometheus_url = os.getenv("MONARCH_PROMETHEUS_URL")
    querier = PrometheusQuerier(prometheus_url)
    
    queries = QUERIES  # This is a dictionary of queries to be executed
    scenario = SCENARIOS["test_with_time"]
    scenario_name = scenario["name"]
    start_time = scenario.get("start_time")
    end_time = scenario.get("end_time")
    kpis = scenario.get("kpis")
    queries = {k: v for k, v in queries.items() if k in kpis}
    logger.info(f"Scenario: {scenario_name}")

    os.makedirs(f"data/{scenario_name}", exist_ok=True)
    for name, query in queries.items():
        logger.info(f"Querying {name}")
        df = querier.query_prometheus(query, start_time, end_time)
        df.to_csv(f"data/{scenario_name}/{name}.csv", index=False)

    logger.info(f"Done! Stored data in data/{scenario_name}")

if __name__ == "__main__":
    main()
