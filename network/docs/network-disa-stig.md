---
layout: demo-detail
demo_slug: network-disa-stig
prerequisites:
  - "Cisco IOS-XE devices in inventory"
  - "Network credentials configured"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "NETWORK | DISA STIG"
    playbook: network/compliance.yml
    description: "Runs DISA STIG compliance checks and hardening on IOS-XE devices"
related_demos:
  - slug: linux-disa-stig
    description: "DISA STIG hardening for RHEL servers"
  - slug: windows-disa-stig
    description: "DISA STIG hardening for Windows servers"
---

Applies DISA STIG compliance checks and hardening to Cisco IOS-XE network devices. Uses the demo.compliance.iosxeSTIG role to evaluate and enforce security controls for network infrastructure.

_Apply DISA STIG compliance to Cisco IOS-XE devices_
