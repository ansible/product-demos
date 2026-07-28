---
layout: demo-detail
demo_slug: openshift-eda-install
---

Deploys an Event-Driven Ansible (EDA) Controller on OpenShift, connected to the same AAP instance. Uses the demo.openshift.eda_controller role to install and configure the operator and custom resource.

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access to the target OpenShift cluster

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift | EDA | Install Controller | [`openshift/eda/install.yml`](https://github.com/ansible/product-demos/blob/main/openshift/eda/install.yml) | Deploys the EDA Controller operator and creates the EDA instance on OpenShift |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Install Operator](/product-demos/demos/openshift-cnv-install/) | Install OpenShift Virtualization alongside EDA |
