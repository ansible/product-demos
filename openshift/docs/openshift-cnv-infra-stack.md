---
layout: demo-detail
demo_slug: openshift-cnv-infra-stack
---

Deploys the full OpenShift CNV infrastructure stack -- installs the OpenShift Virtualization operator, configures cluster settings, provisions RHEL VMs, and syncs the CNV inventory. The OpenShift equivalent of Deploy Cloud Stack in AWS.

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access with bare-metal or nested-virt nodes
- Run <strong>APD | Single demo setup</strong> with <code>openshift</code>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift | CNV | Infra Stack (workflow) | [`openshift/setup.yml`](https://github.com/ansible/product-demos/blob/main/openshift/setup.yml) | Installs CNV, provisions VMs, and syncs inventory in a single workflow |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](/product-demos/demos/openshift-cnv-create-vm/) | Create additional VMs after the stack is deployed |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | The AWS equivalent of this infrastructure workflow |
