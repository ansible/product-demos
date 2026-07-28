---
layout: demo-detail
demo_slug: windows-password-requirements
description: >-
  Configures Windows password policies using PowerShell Desired State
  Configuration (DSC). Sets password history, minimum length, and complexity
  requirements. Demonstrates the integration of Ansible with Windows DSC.
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
job_templates:
  - name: "WINDOWS | Configure Password Requirements"
    playbook: windows/powershell_dsc.yml
    description: "Installs SecurityPolicyDSC module and configures password history, length, and complexity via DSC"
related_demos:
  - slug: windows-disa-stig
    description: "Full STIG hardening which includes password policies and more"
---
