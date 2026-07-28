---
layout: demo-detail
demo_slug: satellite-register
description: >-
  Registers RHEL hosts with a Red Hat Satellite server. Uses the
  demo.satellite.register_host role to configure the Satellite URL, install
  the katello-ca-consumer package, and register the host.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "<strong>Satellite Collection</strong> credential configured"
  - "Run <strong>APD | Single demo setup</strong> with <code>satellite</code>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Register with Satellite"
    playbook: satellite/server_register.yml
    description: "Registers target RHEL hosts with the configured Satellite server"
related_demos:
  - slug: satellite-compliance-scan
    description: "Run compliance scans on Satellite-managed hosts"
  - slug: linux-register-insights
    description: "Register directly with RHSM instead of through Satellite"
---
