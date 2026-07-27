---
layout: demo-detail
demo_slug: openshift-cnv-create-vm
prerequisites:
  - "OpenShift Virtualization installed"
  - "<strong>OpenShift Credential</strong> configured"
  - "RHEL OS images available in openshift-virtualization-os-images namespace"
survey_prompts:
  - question: "VM Name"
    variable: vm_name
    type: text
    required: "Yes"
  - question: "Namespace"
    variable: vm_namespace
    type: text
    required: "Yes"
  - question: "OS Version"
    variable: os_version
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "OpenShift | CNV | Create VM"
    playbook: openshift/cnv/provision_rhel.yml
    description: "Creates a KubeVirt VirtualMachine with a DataVolume from a cluster image source"
related_demos:
  - slug: openshift-cnv-delete-vm
    description: "Delete VMs created by this playbook"
  - slug: openshift-cnv-install
    description: "Install CNV if not already present"
---

Provisions a RHEL virtual machine on OpenShift Virtualization (CNV) using the KubeVirt API. Creates the VM definition with a DataVolume for the OS disk from a cluster image source.

_Provision a RHEL VM on OpenShift Virtualization_
