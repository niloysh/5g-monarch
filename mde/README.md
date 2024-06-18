# MDEs
MDEs allow the NSSDC to collect data from the Network Function (NF) by exposing metrics (such as gtp packets, number of sessions, etc.) via an HTTP endpoint. 

There are two options for setting up the monitoring service: `standard` and `otel` (OpenTelemetry).

The `standard` option uses ServiceMonitors, which are lightweight Kubernetes objects that define the scraping targets for Prometheus. A ServiceMonitor identifies these endpoints and instructs Prometheus to scrape metrics from them. ServiceMonitors themselves do not consume significant resources.

The `otel` option uses the OpenTelemetry Collector, which is a vendor-agnostic implementation that can be used as a metrics (and traces) pipeline. 
This option is useful if we want to do additional processing or export the metrics to multiple monitoring services.

To install the service, run the `install.sh` script with either `standard` or `otel` as the argument, like so:

```bash
./install.sh standard
```