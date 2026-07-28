---
layout: demo-detail
demo_slug: windows-run-powershell
description: >-
  Runs an arbitrary PowerShell script on target Windows hosts. The script
  content is provided via survey. Outputs the results in the job log.
  Demonstrates how Ansible can execute any PowerShell command remotely.
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "PowerShell Script"
    variable: ps_script
    type: textarea
    required: "Yes"
job_templates:
  - name: "WINDOWS | Run PowerShell"
    playbook: windows/powershell.yml
    description: "Executes the provided PowerShell script on target hosts and displays the output"
related_demos:
  - slug: windows-run-powershell-kerberos
    description: "Same playbook but with Kerberos authentication"
  - slug: windows-query-services
    description: "Pre-built PowerShell script for querying services"
---
