---
layout: demo-detail
demo_slug: linux-cockpit
description: >-
  Installs and configures the Cockpit web console on RHEL hosts using RHEL
  System Roles. Cockpit provides a browser-based management interface for
  Linux servers. Demonstrates how System Roles make complex configurations
  repeatable.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Cockpit"
    playbook: linux/system_roles.yml
    description: "Applies the cockpit System Role to install and configure the web console"
related_demos:
  - slug: linux-system-roles
    description: "Apply additional System Roles alongside Cockpit"
---
