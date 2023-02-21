# 5G-MonArch

![GitHub](https://img.shields.io/github/license/niloysh/5g-monarch) ![GitHub forks](https://img.shields.io/github/forks/niloysh/5g-monarch?style=social)

**5G-MonArch** is a network slice monitoring architecture for cloud native 5G network deployments. This repository contains the source code and configuration files for setting up cloud native 5G network slice deployment, based on the Free5GC and UERANSIM projects, along with 5G-MonArch.

[![GitHub](https://img.shields.io/badge/Video-green)](https://www.youtube.com/watch?v=pIMBCwPs0wc) [![GitHub](https://img.shields.io/badge/Download%20Paper-green)](https://niloysaha.me/papers/conferences/2023-noms-monarch.pdf)



# Deploying a basic 5G network

## Dependencies

### Kubernetes
![GitHub](https://img.shields.io/badge/kubernetes-v1.23.6-green)

This deployment leverages Kubernetes for container orchestration. 

For our testbed, we deploy a 4-node Kubernetes cluster, consisting of 1 master node and 3 worker nodes, using the `kubeadm` tool. See the [official Kubernetes installation guide.](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) There are a number of unofficial tutorials on the web for setting up a Kubernetes cluster using `kubeadm` such as [here](https://devopscube.com/setup-kubernetes-cluster-kubeadm/) and [here](https://bikramat.medium.com/set-up-a-kubernetes-cluster-with-kubeadm-508db74028ce).

**Note**: We are using Kubernetes version `1.23.6-00` with Docker as the [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/). From Kubernetes version `1.24` onwards, Kubernetes has deprecated support for Docker as the container runtime, so you may need to use a different container runtime if you are using the latest version of Kubernetes.

**Note**: A common issue you may face is related to kubelet health. This is related to the cgroup driver. Changing the docker driver from `cgroupfs` to `systemd` solves this issue. See this [post on stackoverflow](https://stackoverflow.com/a/68722458/9346339)

### Flannel

![GitHub](https://img.shields.io/badge/Flannel-latest-green)

We use [Flannel](https://github.com/flannel-io/flannel) as the [container network interface](https://github.com/containernetworking/cni)  for inter-cluster networking. Flannel can be easily deployed following the [official instructions here](https://github.com/flannel-io/flannel#deploying-flannel-manually).

### Multus
![GitHub](https://img.shields.io/badge/Multus-latest-green)

Some 5G network functions (e.g., UPF) require multiple interfaces in the container. For this, we use [Multus CNI](https://github.com/k8snetworkplumbingwg/multus-cni). Multus can be installed following the [official instructions here.](https://github.com/k8snetworkplumbingwg/multus-cni)

## Deploying the 5G core, gNodeB, and UEs

![GitHub](https://img.shields.io/badge/UERANSIM-v3.2.6-green) ![GitHub](https://img.shields.io/badge/Free5GC-v3.2.0-green)

To deploy a 5G network, we make leverage the [Free5GC](https://www.free5gc.org/) and [UERANSIM](https://github.com/aligungr/UERANSIM) projects. 

**Note:** The various 5G network functions have been pre-packaged as Docker containers and the Kubernetes manifest files pull the containers hosted on the GitHub container repository. The code for creating the Docker containers for these functions can be found [here](https://github.com/niloysh/free5gc-dockerfiles).

### Setting up the MongoDB database

Free5GC uses mongodb as the database. To ensure that the Kubernetes manifest file for mongodb works, first we need to setup a [local Kubernetes persistent volume.](https://kubernetes.io/docs/concepts/storage/volumes/#local) You can do this by using the `5gc-manifests/create-free5gc-pv.sh` script. It will create a local persistent volume in one of your nodes.

**Note**: You need to edit the `5gc-manifests/free5gc-pv` file as follows

```
local:
    path: /home/n6saha/kubedata **<<=== create this path in one of your nodes!**
nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - nuc2  **<<===== change this to your kubernetes node with the path!**
```

### Setting up gtp5g and labelling the nodes

Free5GC uses the [gtp5g kernel module](https://github.com/free5gc/gtp5g) for UPF packet processing. This needs to be installed on the nodes which will run the UPF.

**Note**: Once gtp5g has been installed on specific nodes, we need to label them so that Kuberenetes can schedule the UPF function on the correct nodes (you can see this in the `nodeAffinity` rules in the UPF deployment files).

Find out your node names and show all node labels: `kubectl get nodes --show-labels` 

Add the label `nodetype` to your nodes which has `gtp5g` installed using `kubectl label node <nodename> nodetype=userplane`

Now you are ready to deploy the 5G network!

### Deploying a basic 5G network and testing connectivity

![slice-x1](/images/slice-x1.png)

First, deploy the Free5GC network to the `test` namespace

```
kubectl apply -f 5gc-manifests/free5gc-v3.2.0-simple --recursive -n test
```

Next, deploy the UERANSIM gNodeB to the test namespace

```
kubectl apply -f 5gc-manifests/ueransim-v3.2.6-gnb --recursive -n test
```

**Note**: Before running the UEs, you have to enter the subscription information using the Free5GC webconsole. The webconsole can be accessed at port `30500` on any of your Kubernetes nodes. The details of the UEs can be found in `free5gc-ue.yaml` in the `5gc-manifests/ueransim-v3.2.6-ue-slice-x3/ueX/ueX-configmap.yaml`. Note that ue1 and ue4 are configured for slice 1 and ue2 and ue5 are configured for slice 2. At this point, we only have slice 1.

![webconsole.png](/images/webconsole.png)

Once the subscribers have been inserted, you can run the UEs. You can deploy ue1 as follows.

```
kubectl apply -f ueransim-v3.2.6-ue-slice-x3/ue1/ --recursive -n test
```

### Utilities

The `5gc-manifests/utils` directory contains some convenience utilities. You can move them to your system path for easier access.

For example, `free5gc-log.sh upf1 upf` will help you see the UPF logs, and `free5gc-log.sh amf` will help you see AMF logs.

You can use  `ueransim-log.sh ue1` to see the UE logs. If you see a TUN interface set up, everything is working correctly and you should be able to ping using the UE.

![ue1.png](/images/ue1.png)

 

![ue1-ping.png](/images/ue1-ping.png)

## Deploying a 5G network with network slicing
Next, we deploy 2 network slices. Each of these slices has a dedicated SMF and UPF, and other 5G core functions are common across slices.

**Note**: Ensure that you have the [basic 5G network setup](#deploying-the-5g-core-gnodeb-and-ues) Deploying a basic 5G network and testing connectivity) working before proceeding with different slicing configurations.


![slice-x2](/images/slice-x2.png)

**Note**: Before proceeding, make sure to remove the the simple network as follows.

```
kubectl delete -f 5gc-manifests/free5gc-v3.2.0-simple --recursive -n test
```

### Deploying 2 network slices
Follow the same procedure to deploy Free5GC, gNB, and UE as before. Use the manifest files named `slice-x2`

```
kubectl apply -f 5gc-manifests/free5gc-v3.2.0-slice-x2 --recursive -n test
```

### Connecting to 2 different slices

The UE configuration files have been setup such that `ue1` and `ue4` are configured for slice 1 and `ue2` and `ue5` are configured for slice 2. Once you deploy `ue1` and `ue2`, they should connect to two different slices and create two PDU sessions, as shown in the figure above.

## Deploying 5G-MonArch

5G-MonArch is a scalable monitoring architecture for 5G, which focuses on network slice monitoring and slice KPI computation. The figure below shows the high-level architecture of 5G-MonArch.

![5g-monarch](/images/5g-monarch.png)

Deploying 5G-MonArch involves deploying its various components, as well as exporters alongside the 5G network functions. 

**Note**: In our deployment, we use a separate 3-node Kubernetes cluster for 5G-MonArch, which connects to the existing 4-node cluster hosting the 5G network. According to your setup, you may need to change the IP addresses of the components.

### Deploying the Data Store

#### ElasticSearch
We use ElasticSearch (ES) as the NoSQL database. The manifest files for installing ElasticSearch are in `monarch-components/data-store/elastic`

**Note**: We use a 3-node ES cluser, and accordingly provision Kubernetes local persistent volumes (See `elasticsearch-local-pv.yaml`). Note that we create a local storageclass called `local-storage` using `monarch-components/local-storageclass.yaml`.


**Note**: Install ES in the `elastic` namespace, as follows:
```
kubectl apply -f monarch-components/data-store/elastic/ -n elastic
```

#### TSDB
We use the same Prometheus database for central TSDB and SSMC. Follow the same steps as SSMC for setting up TSDB. You can connect SSMC and TSDB using  the Prometheus `remote_write` API.

Also see [this note on building hierarchical Prometheus TSDB](https://logz.io/blog/devops/prometheus-architecture-at-scale/)

### Deploy Data Distribution module

#### Apache Kafka
We use Apache Kafka as the broker to receive network slice information from FileBeats installed on the 5G network nodes.

To run Apache Kafka follow the [strimzi documentation](https://strimzi.io/quickstarts/) and apply the `kafka-values.yaml` file. 

**Note**: Ensure you have provisioned a local persistent volume using `kafka-local-pv.yaml` before deploying.

#### Logstash
```
kubectl apply -f monarch-components/data-distribution/logstash/ -n elastic
```

**Note**: The `logstash-cm.yaml` file has the logstash configuration for parsing messages arriving at the Kafka `filebeat` topic and parsing it to extract S-NSSAI.


### Deploy SSMC and Visualization module
We use Prometheus as the SSMC and Grafana as the visualization module.
We use [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) to deploy Prometheus and Grafana using the custom values file `monarch-components/ssmc/kube-prometheus-values-nuc.yaml`.

```
helm install prometheus prometheus-community/kube-prometheus-stack -f kube-prometheus-values-nuc.yaml
```

**Note**: The use of the namespace `monitoring` is very important! This will affect autodiscovery of monitoring exporters.


### Deploy the network slice with monitoring 
5G MonArch uses monitoring data exporters (MDEs) which export monitoring information from the 5G network. To deploy network slices with MDE support, use the following manifest files.

```
kubectl apply -f 5gc-manifests/free5gc-v3.2.0-slice-x2-mon --recursive -n test
```

This will initiate a setup with the following:
- UPF pod now has 3 containers: 1) upf 2) upf-stats which logs upf statistics, and 3) upf-exporter, which exposes upf statistics to SSMC
- SMF pod now has 2 containers: 1) smf and 2) smf-logs which exposes slice information to Filebeats, which then sends it to data distribution (Apache Kafka).

Note that in the screenshot below, there are 2 containers in the SMF pods and 3 containers in the UPF pods.

![slice-x2-up](/images/slice-x2-up.png)

#### Deploy FileBeats
We use FileBeats as an MDE to send the slice information from the SMF to the data distribution module.  

```
kubectl apply -f monarch-components/mde/filebeat-smf.yaml
```

**Note**: A current limitation is that FileBeats does not work in a separate namespace and it needs to run in the `kube-system` namespace. Contributions are welcome on fixing this.

**Note**: Make sure to change your destination address in `filebeat-smf.yaml` file to point to your Kafka endpoint.

```
output.kafka:
      # this should be the Kakfa nodeport service
      hosts: ["129.97.26.28:32100"]   <<=== change this!
      topic: filebeat
```

At this point, if you setup a PDU session and send some traffic though the networks, you should see packet statistics shown in the `upf-stats` container and slice information shown in the `smf-logs` container.

UPF stats should look as below.

![upf-stats](/images/pdr-stats-log.png)

SMF logs shoud look as below.
![smf-logs](/images/smf-logs-log.png)


### Deploy MDE auto discovery mechanism

We use Kubernetes service monitor to enable autodiscovery to MDEs. The following manifest file sets up the service monitor to automatically detect UPF MDEs.

```
kubectl apply -f monarch-components/mde/upf-monitor/
```

**Note**: [Great diagram on how service monitor works](https://stackoverflow.com/a/70453961/9346339)

### Deploy KPI computation module

The KPI computation module pulls data from the data store and computes the network slice throughput KPI. The KPI computation logic can be found in `monarch-components/kpi-computation/slice-throughput.py`. This has been packaged as a container which the `kpi-monitor` manifest file pulls from.

```
kubectl apply -f monarch-components/kpi-computation/kpi-monitor
```

**Note**: You *will* have to change the ElasticSearch and Prometheus endpoints in the kpi-exporter container to make it suitable for your scenario. The code is available [here](https://github.com/niloysh/free5gc-dockerfiles/kpi-monitor).

KPI monitor logs should look like below.

![kpi-monitor](/images/kpi-exporter-log.png)

### Visualizing network slice throughput KPI

Slice thoughput may be visualized in the Grafana dashboard, provided the components above are working correctly.

A pre-configured Grafana dashboard is available in `monarch-components/kpi-computation/visualization/`. You can import the JSON file in Grafana to create the dashboard.

[![grafana-dashboard](/images/grafana-dashboard.png)](https://www.youtube.com/watch?v=pIMBCwPs0wc)


## Credits
These manifest files are heavily inspired from [towards5gs-helm](https://github.com/Orange-OpenSource/towards5gs-helm) and the Docker images used are based on [free5gc-compose](https://github.com/free5gc/free5gc-compose).

## Citation
![GitHub](https://img.shields.io/badge/IEEE%20NOMS-2023-green)

If you use the code in this repository in your research work or project, please consider citing the following publication.

> N. Saha, N. Shahriar, R. Boutaba and A. Saleh. (2023). MonArch: Network Slice Monitoring Architecture for Cloud Native 5G Deployments. In Proceedings of the IEEE/IFIP Network Operations and Management Symposium (NOMS). Miami, Florida, USA, 08 - 12 May, 2023.


## Contributions
Contributions, improvements to documentation,  and bug-fixes are always welcome!
See [first-contributions](https://github.com/firstcontributions/first-contributions).