---
layout: demo-detail
demo_slug: openshift-cnv-install
---

Deploys the OpenShift Virtualization (CNV) operator on an OpenShift cluster, creates the HyperConverged custom resource, and provisions a test VM to verify functionality.

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access with bare-metal or nested-virt capable nodes

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Install | [`openshift/cnv/install.yml`](https://github.com/ansible/product-demos/blob/main/openshift/cnv/install.yml) | Installs the CNV operator, creates HyperConverged CR, and provisions a test VM |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](/product-demos/demos/openshift-cnv-create-vm/) | Create additional VMs after installing CNV |
| ⎈ [CNV — Delete VM](/product-demos/demos/openshift-cnv-delete-vm/) | Clean up VMs when done |
