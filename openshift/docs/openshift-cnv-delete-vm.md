# CNV — Delete VM


Deletes one or more virtual machines from OpenShift Virtualization. Removes the VirtualMachine and associated DataVolume resources. Supports pattern-based host selection for bulk cleanup.

## Prerequisites

- Existing CNV VMs to delete
- <strong>OpenShift Credential</strong> configured


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| VM host string | `vm_host_string` | text | Yes |
| VM NameSpace | `vm_namespace` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Delete VM | [`openshift/cnv/delete.yml`](https://github.com/ansible/product-demos/blob/main/openshift/cnv/delete.yml) | Removes VirtualMachine and DataVolume resources from the specified namespace |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](/product-demos/demos/openshift-cnv-create-vm/) | Create VMs to manage with this playbook |
