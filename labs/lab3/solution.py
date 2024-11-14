import requests
import numpy as np
import logging
import os
from dotenv import load_dotenv

# Logging configuration
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
log.addHandler(console_handler)

# Load environment variables
load_dotenv()
MONARCH_THANOS_URL = os.getenv("MONARCH_THANOS_URL")


def parse_numeric_value_from_prometheus_response(response_json):
    """
    Parse a numeric value from the Prometheus response JSON.
    """
    try:
        results = response_json["data"]["result"]
        values = [float(result["value"][1]) for result in results]
        log.debug(values)
        if values:
            value = np.sum(values)
            return value
        else:
            return None
    except (KeyError, IndexError, ValueError) as e:
        log.error(f"Failed to parse Prometheus response: {e}")

def parse_data_from_prometheus_response(response_json):
    """
    Parse the labels from the Prometheus response JSON.
    """
    try:
        labels = response_json["data"]["result"][0]["metric"]
        return labels
    except (KeyError, IndexError, ValueError) as e:
        log.error(f"Failed to parse Prometheus response: {e}")

def query_prometheus(query, url=MONARCH_THANOS_URL):
    """
    Query Prometheus using requests and return value.
    """
    try:
        params = {'query': query}
        log.debug(params["query"])
        response = requests.get(url + '/api/v1/query', params)
        if response.status_code == 200:
            return response.json()
        else:
            log.error(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        log.error(f"Failed to query Prometheus: {e}")


if __name__ == "__main__":

    ####################### TASK 1: Using the HTTP API with Python #######################

    # Task 1a: Query a sample metric from Prometheus.
    # Here, we query for the number of registered subscribers in the AMF function.
    query = 'fivegs_amffunction_rm_registeredsubnbr'
    response = query_prometheus(query)
    print("Registered subscribers:", response)

    # Task 1b: Count the number of pods in the "open5gs" namespace.
    # Step 1: Write the appropriate query.
    # Hint: Use the `count()` function with `kube_pod_info` and filter by namespace.
    query = 'count(kube_pod_info{namespace="open5gs"})'
    result = query_prometheus(query, MONARCH_THANOS_URL)
    result = parse_numeric_value_from_prometheus_response(result)
    print(f"Number of pods in 'open5gs' namespace: {result}")

    ####################### TASK 2: Retrieve VNFM Metrics ###########################

    # Task 2a: Identify the node where "UPF1" pod is deployed.
    # Write a query to retrieve the node information for the pod "UPF1".
    # Uncomment and complete the code below.
    # Hint: Use `kube_pod_info` and filter with a regex: `{pod=~".*upf1.*"}`
    # 
    query = 'kube_pod_info{pod=~".*upf1.*"}'  # Your query here
    result = query_prometheus(query)
    node_name = parse_data_from_prometheus_response(result).get("node")
    print(f"UPF1 is deployed on node: {node_name}")

    # Task 2b: Check the CPU limit set for the "UPF1" pod.
    # Write a query to get the CPU limits for the "UPF1" pod.
    # Uncomment and complete the code below.
    # Hint: Use `kube_pod_container_resource_limits`.
    #
    query = 'kube_pod_container_resource_limits{pod=~".*upf1.*",resource="cpu"}'  # Your query here
    result = query_prometheus(query)
    result = parse_numeric_value_from_prometheus_response(result)
    print(f"The CPU limit for 'UPF1' pod is {result * 1000} millicores")

    # Task 2c: Find the memory request for the "AMF" pod.
    # Write a query to get the memory request limits for the "AMF" pod.
    # Uncomment and complete the code below.
    # Hint: Use `kube_pod_container_resource_limits`.
    # 
    query = 'kube_pod_container_resource_limits{pod=~".*amf.*",resource="memory"}'  # Your query here
    result = query_prometheus(query)
    result = parse_numeric_value_from_prometheus_response(result)
    print(f"The memory request for 'AMF' pod is {result / 1000000} MB")

    # Task 2d: Measure the CPU usage of the "UPF1" pod.
    # This query has been pre-filled for you. Just uncomment the code below and run it.
    # 
    query = 'rate(container_cpu_usage_seconds_total{pod=~".*upf1.*", container!=""}[1m])'
    result = query_prometheus(query, MONARCH_THANOS_URL)
    result = parse_numeric_value_from_prometheus_response(result)
    print(f"Current CPU usage for 'UPF1' pod is {result * 1000} millicores")

    ################ TASK 3: Compose Slice-Level KPIs ##############################

    # Task 3: Calculate the memory usage percentage for Slice 1 (SNSSAI=1-000001).
    # Step 1: Retrieve the memory requests and usage for SMF1 and UPF1.
    # Use appropriate queries and hints provided to complete each step below.

    # Uncomment and replace `''` with actual queries.

    # Step 1a: Query memory requests for SMF1
    query = 'kube_pod_container_resource_requests{pod=~".*smf1.*",resource="memory"}'  # Your query here (memory requests for SMF1)
    smf1_requested_memory = query_prometheus(query, MONARCH_THANOS_URL)
    smf1_requested_memory = parse_numeric_value_from_prometheus_response(smf1_requested_memory)

    # Step 1b: Query memory usage for SMF1 (this part is pre-filled)
    query = 'avg_over_time(container_memory_working_set_bytes{pod=~".*smf1.*"}[5m])'
    smf1_memory_usage = query_prometheus(query, MONARCH_THANOS_URL)
    smf1_memory_usage = parse_numeric_value_from_prometheus_response(smf1_memory_usage)

    # Step 2a: Query memory requests for UPF1
    query = 'kube_pod_container_resource_requests{pod=~".*upf1.*",resource="memory"}'  # Your query here (memory requests for UPF1)
    upf1_requested_memory = query_prometheus(query, MONARCH_THANOS_URL)
    upf1_requested_memory = parse_numeric_value_from_prometheus_response(upf1_requested_memory)

    # Step 2b: Query memory usage for UPF1
    query = 'avg_over_time(container_memory_working_set_bytes{pod=~".*upf1.*"}[5m])'  # Your query here (memory usage for UPF1)
    upf1_memory_usage = query_prometheus(query, MONARCH_THANOS_URL)
    upf1_memory_usage = parse_numeric_value_from_prometheus_response(upf1_memory_usage)

    # Step 3: Calculate the percentage of requested memory being used.
    # Uncomment and complete the calculations below.
    #
    total_requested_memory = smf1_requested_memory + upf1_requested_memory
    total_memory_usage = smf1_memory_usage + upf1_memory_usage
    percent_memory_used = (total_memory_usage / total_requested_memory) * 100
    print(f"Percentage of requested memory being used by Slice 1 (SMF1 and UPF1): {percent_memory_used:.2f}%")