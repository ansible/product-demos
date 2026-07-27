---
layout: demo-detail
demo_slug: windows-query-services
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Service State"
    variable: service_state
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "WINDOWS | Query Services"
    playbook: windows/powershell_script.yml
    description: "Copies and runs a PowerShell script that filters services by the selected state"
related_demos:
  - slug: windows-run-powershell
    description: "Run arbitrary PowerShell for more complex queries"
---

Copies a PowerShell script to the target host and queries Windows services filtered by state (Running, Stopped, etc.). Demonstrates file transfer and script execution patterns on Windows with Ansible.

_Query Windows services by state using PowerShell_
