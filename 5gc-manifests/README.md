# About
This repository contains Kubernetes manifest files to run a 5G network consisting of 5G core network using the [Free5GC](https://github.com/free5gc/free5gc) project and RAN using the [UERANSIM](https://github.com/aligungr/UERANSIM) project.

# Installation
1. You need to have a working kubernetes cluster. Instructions for setting up a multi-node Kubernetes cluster is available in the [official docs](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/). Note that we are using `kubeadm=1.23.6-00 kubectl=1.23.6-00 kubelet=1.23.6-00` as this is the last version that supports Docker as a container runtime out of the box. If you are using the latest Kubernetes with docker, see instructions [here](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#docker).

2. You need to install [Flannel CNI](https://github.com/flannel-io/flannel) and [Multus CNI](https://github.com/k8snetworkplumbingwg/multus-cni). Flannel is used for cluster networking. Multus CNI enables attaching multiple network interfaces to pods in Kubernetes, which is required for 5G NFs with multiple interfaces (e.g., UPF has the N3 interface towards gNB and the N4 interface towards SMF).

3. You need to create a local persistent volume for MongoDB. Free5GC uses MongoDB for storage. This can be created using the `create-free5gc-pv.sh` script.
Note that you need to change the `path` and `values` in the `free5gc-pv.yaml` file according to your cluster.

4. The Multus CNI interfaces in the manifests, denoted by `k8s.v1.cni.cncf.io/networks` in the deployment files have static IPs assigned to them according to our lab setup (129.97.168.0/24 subnet). All these IPs need to be changed according your scenario. Use an IP range that you can access from all nodes of your Kubernetes cluster.

5. The Free5GC core can be installed as follows:
```
kubectl apply -f free5gc-v3.2.0 --recursive -n <namespace>
```
and uninstalled using:
```
kubectl delete -f free5gc-v3.2.0 --recursive -n <namespace>
```
6. The RAN (gNB + UE) can be installed as follows:
```
kubectl apply -f ueransim-v3.2.6 --recursive -n <namespace>
```
and uninstalled using:
```
kubectl delete -f ueransim-v3.2.6 --recursive -n <namespace>
```
   

# Which manifest file should I use?
Directories with have the term `slice` in them contain manifests for creating multiple slices. For example, `slice-x2` represents two slices.
## Single Slice
- free5gc-v3.0.5 is working with ueransim-v3.1.3.
- free5gc-v3.2.0 working with ueranim-v3.2.6.
## Multiple Slices

- free5gc-v3.0.5-slice-x2 has issues with SMF selection for the 2nd slice. 
Contributions welcome for fixing it and/or finding out why the errors occur.
- free5gc-v3.2.0-slice-x2 is working with ueransim-v3.2.6.

# Running into issues!
The manifest files are not working? Please see the [FAQ](FAQ.md).


# Credits
These manifest files are heavily inspired from [towards5gs-helm](https://github.com/Orange-OpenSource/towards5gs-helm) and the Docker images used are based on [free5gc-compose](https://github.com/free5gc/free5gc-compose).
   
