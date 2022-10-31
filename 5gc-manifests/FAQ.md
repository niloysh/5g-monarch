# FAQs

### The mongodb container is stuck at pending?

   Make sure the local persistent volume is available. This can be checked using `kubectl get pv`. Note that uninstalling the manifests does not delete the persistent volume claim (pvc) for mongodb. This may cause mongodb to get stuck in pending state. In this case, delete the pvc, then delete and re-create the pv. See more about [Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

### How do I update container images to the latest version?

   The container images are hosted on Github container registry and can be found linked to [this repository](https://github.com/niloysh/free5gc-dockerfiles), which also contains the Dockerfiles used to build the images.
   You can use the Dockerfiles to update the images to the latest version. Please note that you will have to update the corresponding configuration files in the manifests, according to the version of Free5GC or UERANSIM being used.

### SCTP connection refused for UERANSIM gNB?

   See this [issue](https://github.com/aligungr/UERANSIM/issues/302) on UERANSIM GitHub page.
   Also, check if the IP the AMF is listening on is available. Use nmap to scan the network.

### UPF stuck at container creating?

   If there are MACVLAN errors and the like, remember that we need to change the global master interface parameters in the to match the primary network interface of the Kubernetes hosts. This can be found in `5gnetwork.yaml` file, where the master interface is `eno1` in our setup.

### ImagePullError in Kubernetes pods?

   Check that the DNS is working in the nodes which are hosting the functions which have errors.
   For instructions on DNS override (in case netplan is not working), see [this link](https://unix.stackexchange.com/questions/588658/override-ubuntu-20-04-dns-using-systemd-resolved).

### Free5GC Gtp5g error?

   Check that the gtp5g module is loaded properly. See instructions [here](https://github.com/free5gc/gtp5g#compile). The module is set to load automatically on boot in `/etc/modules`. 
   
   **Module not working**: The issue is that the module was place in `/lib/modules/<kernel_version>/kernel/drivers/net`. However, if the `kernel_version` got updated, such as from `5.4.0-104-generic` to `5.4.0-109-generic`, the module could not be found. A workaround for this may be to hold the kernel upgrades. See this [stack-overflow post.](https://askubuntu.com/questions/938494/how-to-i-prevent-ubuntu-from-kernel-version-upgrade-and-notification). Note that doing this opens up your system to security vulnerabilities; do this at your own risk.

### Can't change name of SMF service?

   If I change the name of smf service from `smf-nsmf` to `smf1-nsmf` we get a server no response from the AMF.

   **Why is this happening?** This is because MongoDB is storing information related to the SMF instance. To fix, delete the pvc, then the pv, then *delete the directory being used for local storage*. Then recreate the pv. See [here](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for more information on Kubernetes persistent volumes.

### Two UPFs don't work together?

      Two UPFs won't run on the same node. We need some kind of affinity rules (to make sure UPF runs on nodes with gtp5g installed) anti-affinity rules (to make sure only 1 UPF runs on a given node) in place (this is included in the manifest files). If this is not working, check your pod and node labels.

### UPF stuck at pending?

   The manifest files contain node affinity rules so that UPF pods are only scheduled on nodes with gtp5g installed on them. This is achieved by labelling Kubernetes nodes with the label "nodetype=userplane". See the [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) for more information on using labels and selectors.

