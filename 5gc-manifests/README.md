# 5G-MonArch

![GitHub](https://img.shields.io/github/license/niloysh/5g-monarch) ![GitHub forks](https://img.shields.io/github/forks/niloysh/5g-monarch?style=social)

**5G-MonArch** is a network slice monitoring architecture for cloud native 5G network deployments. This repository contains the source code and configuration files for setting up cloud native 5G network slice deployment, based on the Free5GC and UERANSIM projects, along with 5G-MonArch.

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

## Deploying a 5G network

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

Now you are ready to deploy the 5G network

### Deploying a basic 5G network and testing connectivity

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

### Deploying 2 network slices

## Deploying 5G-Monarch

### Deploying central database, logstash,

### Deploy SSMC and visualization module

### Deploy the network slice with monitoring support

### Deploy MDE auto discovery mechanism

upf-monitor

### Deploy KPI computation module

kpi-exporter 

### Visualizing network slice throughput KPI

Grafana and dashboard
