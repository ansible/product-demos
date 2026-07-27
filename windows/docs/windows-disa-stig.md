---
layout: demo-detail
demo_slug: windows-disa-stig
prerequisites:
  - "Windows Server 2022 hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: HOSTS
    type: text
    required: "Yes"
job_templates:
  - name: "WINDOWS | DISA STIG"
    playbook: windows/compliance.yml
    description: "Applies Windows 2022 DISA STIG hardening controls from the demo.compliance collection"
related_demos:
  - slug: linux-disa-stig
    description: "DISA STIG hardening for RHEL servers"
  - slug: windows-password-requirements
    description: "Lighter-weight password policy configuration via DSC"
---

Applies DISA STIG hardening to Windows Server 2022. Uses the demo.compliance.win2022STIG role to configure security controls required for U.S. Department of Defense Windows environments.

_Apply DISA STIG hardening to Windows Server 2022_
