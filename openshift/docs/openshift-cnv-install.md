---
layout: demo-detail
demo_slug: openshift-cnv-install
description: >-
  Deploys the OpenShift Virtualization (CNV) operator on an OpenShift cluster,
  creates the HyperConverged custom resource, and provisions a test VM to
  verify functionality.
prerequisites:
  - "<strong>OpenShift Credential</strong> configured with API token"
  - "Cluster admin access with bare-metal or nested-virt capable nodes"
job_templates:
  - name: "OpenShift | CNV | Install"
    playbook: openshift/cnv/install.yml
    description: "Installs the CNV operator, creates HyperConverged CR, and provisions a test VM"
related_demos:
  - slug: openshift-cnv-create-vm
    description: "Create additional VMs after installing CNV"
  - slug: openshift-cnv-delete-vm
    description: "Clean up VMs when done"
---
