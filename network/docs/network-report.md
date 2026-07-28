---
layout: demo-detail
demo_slug: network-report
description: >-
  Generates an HTML network report by gathering facts from Cisco IOS, IOS-XR,
  and NX-OS devices. Collects interface, routing, and system information using
  the platform-specific facts modules and renders them into a browsable
  report.
prerequisites:
  - "Network devices in inventory"
  - "Network credentials configured"
  - "A <code>reports</code> host for publishing the HTML report"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "NETWORK | Report"
    playbook: network/report.yml
    description: "Gathers facts from Cisco IOS, IOS-XR, and NX-OS devices and generates an HTML report"
related_demos:
  - slug: network-configuration
    description: "Apply configurations before generating a report"
  - slug: network-backup
    description: "Back up configurations alongside reporting"
---
