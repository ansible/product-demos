---
layout: demo-detail
demo_slug: openshift-cnv-patch-workflow
description: >-
  Patching workflow for RHEL VMs running on OpenShift Virtualization. Similar
  to the cloud patching workflow but targeting CNV-managed virtual machines
  instead of EC2 instances.
prerequisites:
  - "RHEL VMs provisioned on OpenShift CNV"
  - "<strong>OpenShift Credential</strong> configured"
  - "SSH connectivity to the CNV VMs"
job_templates:
  - name: "OpenShift | CNV | Patch Workflow"
    playbook: openshift/setup.yml
    description: "Runs the patching workflow against CNV-managed RHEL virtual machines"
related_demos:
  - slug: patch-cloud-stack
    description: "The AWS version of this patching workflow"
  - slug: openshift-cnv-infra-stack
    description: "Deploy the CNV infrastructure to patch"
---
