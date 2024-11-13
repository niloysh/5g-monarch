### Task 3: Using the Thanos HTTP API with Python

Using Python’s HTTP requests library, you can programmatically access Thanos metrics for more flexible data manipulation and analysis. This approach lets you combine, filter, and analyze metrics, which is especially useful for complex metrics like resource utilization across network functions.
1.	Open [exercise.py](exercise.py): This file contains a skeleton of code for **Tasks 3 through 5**.
2.	Structure of the Exercise Code:
	- `query_prometheus`: Sends a Prometheus query to the Thanos HTTP API.
	- `parse_numeric_value_from_prometheus_response`: Parses numeric results from the API response.
	- `parse_data_from_prometheus_response`: Parses return data (raw) from the API response.

3. Example query in python

In exercise.py you will find the following snippet, showing an example of using the HTTP API.

```python
query = 'fivegs_amffunction_rm_registeredsubnbr'
response = query_prometheus(query)
print(response)
```

**Task**: Try running this code to see the raw JSON response from the API.

### Task 4: Retrieve VNFM Metrics for Resource Utilization

1.	**Pod Status and Resource Utilization**: VNFM metrics can provide insights into the health of 5G network functions by monitoring the status of Kubernetes pods and resource utilization.

2.	**Query Example**: Query metrics like `kube_pod_info` and `kube_pod_container_resource_requests` to get details about the network functions' CPU and memory usage.

**Exercise**: Modify the code to retrieve CPU and memory usage data, then parse and display it in a readable format.


### Task 5: Compose Slice-Level KPIs


We've already explored examples of slice-level metrics, like `slice_throughput`. Our KPI computation module leverages the Python HTTP API to query raw metrics, calculate KPIs at the slice level, and store them back in a `data_store`, making them accessible for visualization in Grafana.

In this exercise, you'll dive deeper into composing slice-level metrics, specifically focusing on calculating resource utilization for slice 1 (with SNSSAI=1-000001). You'll combine multiple queries to determine memory usage, providing a practical understanding of how to build KPIs from various metric sources.

1. Retrieve Memory Requests:
    - Query kube_pod_container_resource_requests to get memory requests for SMF1 and UPF1.
    - Parse and store these values.
2. Retrieve Memory Usage:
    - Use `avg_over_time(container_memory_working_set_bytes{pod=~".*smf1.*"}[5m])` to find the 5-minute average memory usage for SMF1.
	- Do the same for UPF1.
3. Calculate the Percentage:
    - Sum the memory requests and usage for both SMF1 and UPF1.
	- Calculate the percentage of requested memory currently being used.

