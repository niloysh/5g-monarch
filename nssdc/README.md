# nssdc

## Installation

Create a `thanos-objstore-config.yaml` file in the `nssdc` directory with the following content:

```yaml
type: s3
config:
  bucket: monarch-thanos
  endpoint: "<remote_ip>:<remote_url>"
  access_key: <access_key>
  secret_key: <secret_key>
  insecure: true
```
