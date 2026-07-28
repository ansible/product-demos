---
layout: demo-detail
demo_slug: openshift-cnv-delete-vm
---

Deletes one or more virtual machines from OpenShift Virtualization. Removes the VirtualMachine and associated DataVolume resources. Supports pattern-based host selection for bulk cleanup.

## Prerequisites

- Existing CNV VMs to delete
- <strong>OpenShift Credential</strong> configured

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift | CNV | Delete VM | [`openshift/cnv/delete.yml`](https://github.com/ansible/product-demos/blob/main/openshift/cnv/delete.yml) | Removes VirtualMachine and DataVolume resources from the specified namespace |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](/product-demos/demos/openshift-cnv-create-vm/) | Create VMs to manage with this playbook |
