---
layout: demo-detail
demo_slug: linux-register-insights
description: >-
  Registers RHEL EC2 instances with Red Hat Subscription Manager using an
  activation key and org ID. Removes RHUI packages, installs
  subscription-manager, sets the hostname, and registers the host. Required
  before RHEL advisory patching.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
  - "<strong>RHSM Registration</strong> credential with org ID and activation key"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Register with Insights"
    playbook: linux/ec2_register.yml
    description: "Registers RHEL hosts with RHSM, removes RHUI packages, and configures subscription access"
related_demos:
  - slug: patch-cloud-stack
    description: "RHSM registration is required for RHEL patching in this workflow"
  - slug: linux-patching
    description: "Patch hosts after registering them"
---
