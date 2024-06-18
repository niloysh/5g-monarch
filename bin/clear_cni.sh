#!/bin/bash
# https://docs.microfocus.com/doc/OMT/2022.11/FailToCreatePodSandBox
systemctl stop kubelet
systemctl stop containerd
ls /var/lib/cni/networks/
mv /var/lib/cni/networks /var/lib/cni/networks.bak
mkdir /var/lib/cni/networks
systemctl start containerd
systemctl start kubelet