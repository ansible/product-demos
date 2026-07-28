---
layout: demo-detail
demo_slug: windows-chocolatey-specific
description: >-
  Installs a specific package by name using the Chocolatey package manager.
  The package name is provided via survey. Demonstrates targeted software
  installation on Windows.
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
  - "Internet access from the Windows hosts"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Package Name"
    variable: package_name
    type: text
    required: "Yes"
job_templates:
  - name: "WINDOWS | Chocolatey Install Specific"
    playbook: windows/windows_choco_specific.yml
    description: "Installs a single named package via Chocolatey"
related_demos:
  - slug: windows-chocolatey-multiple
    description: "Install multiple packages at once"
---
