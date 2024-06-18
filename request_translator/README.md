# request-translator
This component implements an abstraction layer that translates high-level monitoring requests specified by the monitoring API into low-level monitoring directives understood by the Monitoring Manager (e.g., which NF instance to monitor).

For now, it uses Kubernetes API as service orchestrator.

## How to run
First, we need to create a secret for the kubeconfig file. This is necessary to access the Kubernetes cluster. The secret is created by running the following script:

```bash
create-kubeconfig-secret.sh
```

**Note**: The script should be updated to point to the correct kubeconfig file.
