QUERIES = {
    # Query to calculate the throughput by slicing data volume on N3 interface
    # for a given Session Establishment ID (SEID), accounting for the session's S-NSSAI.
    "slice_throughput": '''
        sum by (seid) (
            rate(fivegs_ep_n3_gtp_indatavolumen3upf_seid[1m])
            * on (seid) group_right
            sum(fivegs_smffunction_sm_seid_session{snssai="1-000001"}) by (seid, snssai)
        ) * 8
    ''',

    # Query to calculate the CPU usage of the UPF component,
    # normalized by the CPU resources requested for the UPF container.
    "upf_cpu_usage": '''
        rate(container_cpu_usage_seconds_total{
            namespace="open5gs",
            container="upf",
            pod=~".*upf1.*"
        }[1m])
        / on() group_left()
        kube_pod_container_resource_requests{
            resource="cpu",
            namespace="open5gs",
            container="upf",
            pod=~".*upf1.*"
        }
    ''',

    # Query to fetch the current memory usage of the UPF component.
    "upf_memory_usage": '''
        container_memory_working_set_bytes{
            namespace="open5gs",
            pod="open5gs-upf1-555878cc65-bpf8f",
            job="kubelet",
            container="upf"
        }
    ''',

    # Query to calculate the energy consumption of the UPF component.
    "upf_energy_consumption": '''
        sum by (pod_name) (
            rate(kepler_container_joules_total{pod_name=~".*upf1.*"}[1m])
        )
    ''',

    # Query to calculate the CPU usage of the SMF component,
    # normalized by the CPU resources requested for the SMF container.
    "smf_cpu_usage": '''
        rate(container_cpu_usage_seconds_total{
            namespace="open5gs",
            container="smf",
            pod=~".*smf1.*"
        }[1m])
        / on() group_left()
        kube_pod_container_resource_requests{
            resource="cpu",
            namespace="open5gs",
            container="smf",
            pod=~".*smf1.*"
        }
    ''',

    # Query to fetch the duration of the scraping process for the UPF component metrics.
    "upf_scrape_duration": '''
        scrape_duration_seconds{
            namespace="open5gs",
            pod="open5gs-upf1-555878cc65-bpf8f"
        }
    ''',
    "temperature": '''temperature_mde_celsius{mde="mde-1s"}'''
}

SCENARIOS = {
    "cloud_gaming": {
        "name": "cloud_gaming",
        "description": "Cloud gaming dataset replayed through the 5G testbed.",
        "kpis": ["slice_throughput"],
        "start_time": "2023-12-06 13:00:00",
        "end_time": "2023-12-06 16:30:00"
    },
    "test": {
        "name": "test",
        "description": "Test scenario.",
        "kpis": ["temperature"]
    },
    "test_with_time": {
        "name": "test_with_time",
        "description": "Test scenario with start and end time.",
        "kpis": ["temperature", "upf_cpu_usage"],
        "start_time": "2024-02-17 15:00:00",
        "end_time": "2024-02-17 15:20:00"
    }
}

