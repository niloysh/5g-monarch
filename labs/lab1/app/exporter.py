from prometheus_client import start_http_server, Gauge
import random
import time

RESPONSE_TIME = Gauge('workshop_response_time_seconds', 'Response time in seconds', ['service', 'region'])

# Initial response times for each service and region
metric_values = {
    ('auth_service', 'us-west'): 0.5,
    ('auth_service', 'us-east'): 0.6,
    ('payment_service', 'us-west'): 0.8,
    ('payment_service', 'us-east'): 0.9,
}

def adjust_value(current_value, min_value, max_value, fluctuation=0.05):
    """Adjust the value slightly within a defined range."""
    change = random.uniform(-fluctuation, fluctuation)  # Small fluctuation
    new_value = current_value + change
    return max(min_value, min(max_value, new_value))

def collect_simulated_metrics():
    """Simulate gradual changes in response time for each service and region."""
    for (service, region), response_time in metric_values.items():
        metric_values[(service, region)] = adjust_value(response_time, 0.1, 1.0)

        # add labels to Gauge and set values
        RESPONSE_TIME.labels(service=service, region=region).set(metric_values[(service, region)])

if __name__ == '__main__':
    # Start up the server to expose metrics at http://localhost:8000/metrics
    start_http_server(8000)
    print("Serving workshop metrics at http://localhost:8000/metrics")

    # Collect and update metrics every 5 seconds
    while True:
        collect_simulated_metrics()
        time.sleep(5)