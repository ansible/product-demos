---
layout: demo-detail
demo_slug: openshift-cnv-delete-vm
prerequisites:
  - "Existing CNV VMs to delete"
  - "<strong>OpenShift Credential</strong> configured"
job_templates:
  - name: "OpenShift | CNV | Delete VM"
    playbook: openshift/cnv/delete.yml
    description: "Removes VirtualMachine and DataVolume resources from the specified namespace"
related_demos:
  - slug: openshift-cnv-create-vm
    description: "Create VMs to manage with this playbook"
---

Deletes one or more virtual machines from OpenShift Virtualization. Removes the VirtualMachine and associated DataVolume resources. Supports pattern-based host selection for bulk cleanup.

_Delete VMs from OpenShift Virtualization_
