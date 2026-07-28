---
layout: demo-detail
demo_slug: satellite-compliance-scan
description: >-
  Runs OpenSCAP compliance scans on Satellite-managed hosts and uploads
  results to Satellite. Uses the demo.satellite.scap_client role to install
  and configure the foreman_scap_client.
prerequisites:
  - "Hosts registered with Satellite"
  - "Compliance policies configured in Satellite"
  - "<strong>Satellite Collection</strong> credential configured"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | OpenSCAP Scan (Satellite)"
    playbook: satellite/server_openscap.yml
    description: "Installs foreman_scap_client, runs compliance scans, and uploads results to Satellite"
related_demos:
  - slug: satellite-register
    description: "Register hosts with Satellite before scanning"
  - slug: linux-compliance-report
    description: "Local OpenSCAP scanning without Satellite"
---
