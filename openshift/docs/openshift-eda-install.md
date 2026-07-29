# EDA — Install Controller


Deploys an Event-Driven Ansible (EDA) Controller on OpenShift, connected to the same AAP instance. Uses the demo.openshift.eda_controller role to install and configure the operator and custom resource.

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access to the target OpenShift cluster

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ EDA ǀ Install Controller | [`openshift/eda/install.yml`](../eda/install.yml) | Deploys the EDA Controller operator and creates the EDA instance on OpenShift |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Install Operator](./openshift-cnv-install.md) | Install OpenShift Virtualization alongside EDA |
