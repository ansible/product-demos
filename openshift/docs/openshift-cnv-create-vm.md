# CNV — Create RHEL VM


Provisions a RHEL virtual machine on OpenShift Virtualization (CNV) using the KubeVirt API. Creates the VM definition with a DataVolume for the OS disk from a cluster image source.

## Prerequisites

- OpenShift Virtualization installed
- **OpenShift Credential** configured
- RHEL OS images available in openshift-virtualization-os-images namespace

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| VM Name | `vm_name` | text | Yes |
| Namespace | `vm_namespace` | text | Yes |
| OS Version | `os_version` | multiplechoice | Yes |
| SSH Authorized Key | `ssh_authorized_key` | textarea | Yes |
| RHEL Activation Key | `rh_subscription_key` | text | Yes |
| RHEL Organization ID | `rh_subscription_org` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Create VM | [`openshift/cnv/provision_rhel.yml`](../cnv/provision_rhel.yml) | Creates a KubeVirt VirtualMachine with a DataVolume from a cluster image source |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Delete VM](./openshift-cnv-delete-vm.md) | Delete VMs created by this playbook |
| ⎈ [CNV — Install Operator](./openshift-cnv-install.md) | Install CNV if not already present |
