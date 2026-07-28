---
layout: demo-detail
demo_slug: linux-disa-stig
description: >-
  Applies DISA STIG (Security Technical Implementation Guide) hardening to
  RHEL hosts. Uses the demo.compliance collection STIG role to configure
  security controls required for U.S. Department of Defense environments.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | DISA STIG"
    playbook: linux/disa_stig.yml
    description: "Applies DISA STIG hardening controls from the demo.compliance collection"
related_demos:
  - slug: linux-compliance-workflow
    description: "Full compliance workflow with scanning and enforcement"
  - slug: linux-compliance-report
    description: "Generate a compliance report to measure STIG compliance"
---
