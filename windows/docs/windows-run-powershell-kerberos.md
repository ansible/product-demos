---
layout: demo-detail
demo_slug: windows-run-powershell-kerberos
description: >-
  Runs a PowerShell script on Windows hosts using Kerberos authentication
  instead of basic WinRM. Demonstrates Ansible ability to authenticate via
  Active Directory credentials for domain-joined environments.
prerequisites:
  - "Windows hosts joined to an Active Directory domain"
  - "Kerberos credential configured in AAP"
  - "Domain controller reachable from AAP"
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
  - name: "WINDOWS | Run PowerShell | Kerberos"
    playbook: windows/powershell.yml
    description: "Executes PowerShell on target hosts using Kerberos authentication"
related_demos:
  - slug: windows-run-powershell
    description: "Same playbook with standard WinRM authentication"
  - slug: windows-setup-ad-domain
    description: "Set up an AD domain for Kerberos authentication"
---
