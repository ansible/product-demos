---
layout: demo-detail
demo_slug: openshift-cnv-infra-stack
description: >-
  Deploys the full OpenShift CNV infrastructure stack -- installs the
  OpenShift Virtualization operator, configures cluster settings, provisions
  RHEL VMs, and syncs the CNV inventory. The OpenShift equivalent of Deploy
  Cloud Stack in AWS.
prerequisites:
  - "<strong>OpenShift Credential</strong> configured with API token"
  - "Cluster admin access with bare-metal or nested-virt nodes"
  - "Run <strong>APD | Single demo setup</strong> with <code>openshift</code>"
job_templates:
  - name: "OpenShift | CNV | Infra Stack (workflow)"
    playbook: openshift/setup.yml
    description: "Installs CNV, provisions VMs, and syncs inventory in a single workflow"
related_demos:
  - slug: openshift-cnv-create-vm
    description: "Create additional VMs after the stack is deployed"
  - slug: deploy-cloud-stack
    description: "The AWS equivalent of this infrastructure workflow"
---
