---
layout: demo-detail
demo_slug: network-configuration
prerequisites:
  - "Network devices in inventory (Cisco IOS, IOS-XR, and/or NX-OS)"
  - "Network credentials configured"
  - "Run <strong>APD | Single demo setup</strong> with <code>network</code>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "NETWORK | Configuration"
    playbook: (Network Golden Configs project)
    description: "Applies golden configurations to network devices using Ansible resource modules"
related_demos:
  - slug: network-report
    description: "Generate a network report after applying configurations"
  - slug: network-backup
    description: "Back up device configs before making changes"
---

Deploys golden configurations to Cisco IOS, IOS-XR, and NX-OS network devices using Ansible resource modules. Pulls configurations from a separate Git repository (Network Golden Configs) and applies them to the network devices.

_Push golden configs to Cisco IOS, IOS-XR, and NX-OS_
