---
layout: demo-detail
demo_slug: linux-troubleshoot
description: >-
  Gathers quick diagnostic information from RHEL hosts -- vmstat for
  CPU/memory/swap, top processes by CPU usage, and top processes by memory
  usage. A handy first-response playbook for investigating performance issues.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Troubleshoot"
    playbook: linux/tshoot.yml
    description: "Runs vmstat, ps by CPU, and ps by memory on target hosts and displays results"
related_demos:
  - slug: linux-fact-scan
    description: "Gather broader system facts including packages and services"
  - slug: linux-run-shell-script
    description: "Run ad-hoc commands for deeper investigation"
---
