# CNV — Install Operator


Deploys the OpenShift Virtualization (CNV) operator on an OpenShift cluster, creates the HyperConverged custom resource, and provisions a test VM to verify functionality.

## Prerequisites

- **OpenShift Credential** configured with API token
- Cluster admin access with bare-metal or nested-virt capable nodes

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Install | [`openshift/cnv/install.yml`](../cnv/install.yml) | Installs the CNV operator, creates HyperConverged CR, and provisions a test VM |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](./openshift-cnv-create-vm.md) | Create additional VMs after installing CNV |
| ⎈ [CNV — Delete VM](./openshift-cnv-delete-vm.md) | Clean up VMs when done |
