---
layout: demo-detail
demo_slug: linux-system-roles
description: >-
  Applies one or more RHEL System Roles to target hosts. System Roles are a
  collection of Ansible roles for configuring common RHEL subsystems
  (timesync, network, storage, etc.) in a consistent, supported way.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "System Roles"
    variable: system_roles
    type: multiselect
    required: "Yes"
job_templates:
  - name: "LINUX | System Roles"
    playbook: linux/system_roles.yml
    description: "Applies selected RHEL System Roles (timesync, network, storage, etc.) to target hosts"
related_demos:
  - slug: linux-cockpit
    description: "Install Cockpit web console using System Roles"
---
