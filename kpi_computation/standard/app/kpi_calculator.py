#----------------------------------------------------------------------------
# Author: Niloy Saha
# Email: niloysaha.ns@gmail.com
# version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Prometheus exporter which exports slice throughput KPI.
For use with the 5G-MONARCH project and Open5GS.
"""
import os
import logging
import time
import requests
import prometheus_client as prom
import argparse

from dotenv import load_dotenv

load_dotenv()
MONARCH_THANOS_URL = os.getenv("MONARCH_THANOS_URL")
DEFAULT_UPDATE_PERIOD = 1
UPDATE_PERIOD = int(os.environ.get('UPDATE_PERIOD', DEFAULT_UPDATE_PERIOD))
EXPORTER_PORT = 9000
TIME_RANGE = os.getenv("TIME_RANGE", "5s")


# Prometheus variables
SLICE_THROUGHPUT = prom.Gauge('slice_throughput', 'throughput per slice (bits/sec)', ['snssai', 'seid', 'direction'])
# get rid of bloat
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

def query_prometheus(params, url):
    """
    Query Prometheus using requests and return value.
    params: The parameters for the Prometheus query.
    url: The URL of the Prometheus server.
    Returns: The result of the Prometheus query.
    """
    try:
        r = requests.get(url + '/api/v1/query', params)
        data = r.json()

        results = data["data"]["result"]
        return results
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to query Prometheus: {e}")
    except (KeyError, IndexError, ValueError) as e:
        log.error(f"Failed to parse Prometheus response: {e}")
        log.warning("No data available!")

def get_slice_throughput_per_seid_and_direction(snssai, direction):
    """
    Queries both the SMF and UPF to get the throughput per SEID and direction.
    Returns a dictionary of the form {seid: value (bits/sec)}
    """
    time_range = TIME_RANGE
    throughput_per_seid = {}  # {seid: value (bits/sec)}

    direction_mapping = {
        "uplink": "outdatavolumen3upf",
        "downlink": "indatavolumen3upf"
    }

    if direction not in direction_mapping:
        log.error("Invalid direction")
        return

    query = f'sum by (seid) (rate(fivegs_ep_n3_gtp_{direction_mapping[direction]}_seid[{time_range}]) * on (seid) group_right sum(fivegs_smffunction_sm_seid_session{{snssai="{snssai}"}}) by (seid, snssai)) * 8'
    log.debug(query)
    params = {'query': query}
    results = query_prometheus(params, MONARCH_THANOS_URL)

    if results:
        for result in results:
            seid = result["metric"]["seid"]
            value = float(result["value"][1])
            throughput_per_seid[seid] = value

    return throughput_per_seid

   
def get_active_snssais():
    """
    Return a list of active SNSSAIs from the SMF.
    """
    time_range = TIME_RANGE
    query = f'sum by (snssai) (rate(fivegs_smffunction_sm_seid_session[{time_range}]))'
    log.debug(query)
    params = {'query': query}
    results = query_prometheus(params, MONARCH_THANOS_URL)
    active_snssais = [result["metric"]["snssai"] for result in results]
    return active_snssais

def main():
    log.info("Starting Prometheus server on port {}".format(EXPORTER_PORT))

    if not MONARCH_THANOS_URL:
        log.error("MONARCH_THANOS_URL is not set")
        return 

    log.info(f"Monarch Thanos URL: {MONARCH_THANOS_URL}")
    log.info(f"Time range: {TIME_RANGE}")
    log.info(f"Update period: {UPDATE_PERIOD}")
    prom.start_http_server(EXPORTER_PORT)

    while True:
        try:
            run_kpi_computation()
        except Exception as e:
            log.error(f"Failing to run KPI computation: {e}")
        time.sleep(UPDATE_PERIOD)

def export_to_prometheus(snssai, seid, direction, value):
    value_mbits = round(value / 10 ** 6, 6)
    log.info(f"SNSSAI={snssai} | SEID={seid} | DIR={direction:8s} | RATE (Mbps)={value_mbits}")
    SLICE_THROUGHPUT.labels(snssai=snssai, seid=seid, direction=direction).set(value)

def run_kpi_computation():
    directions = ["uplink", "downlink"]
    active_snssais = get_active_snssais()
    if not active_snssais:
        log.warning("No active SNSSAIs found")
        return
    
    log.debug(f"Active SNSSAIs: {active_snssais}")
    for snssai in active_snssais:
        for direction in directions:
            throughput_per_seid = get_slice_throughput_per_seid_and_direction(snssai, direction)
            for seid, value in throughput_per_seid.items():
                export_to_prometheus(snssai, seid, direction, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KPI calculator.')
    parser.add_argument('--log', default='info', help='Log verbosity level. Default is "info". Options are "debug", "info", "warning", "error", "critical".')

    args = parser.parse_args()

    # Convert log level from string to logging level
    log_level = getattr(logging, args.log.upper(), None)
    if not isinstance(log_level, int):
        raise ValueError(f'Invalid log level: {args.log}')
    
    # setup logger for console output
    log = logging.getLogger(__name__)
    log.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    log.addHandler(console_handler)
        
    main()

    
    


