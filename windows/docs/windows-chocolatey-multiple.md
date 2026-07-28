---
layout: demo-detail
demo_slug: windows-chocolatey-multiple
description: >-
  Installs multiple packages (Node.js and Python by default) using the
  Chocolatey package manager. Verifies the installations by checking version
  output. Demonstrates bulk software provisioning on Windows with Ansible.
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
  - "Internet access from the Windows hosts"
job_templates:
  - name: "WINDOWS | Chocolatey Install Multiple"
    playbook: windows/windows_choco_multiple.yml
    description: "Installs Node.js and Python via Chocolatey and verifies the installed versions"
related_demos:
  - slug: windows-chocolatey-specific
    description: "Install a single specific package via Chocolatey"
  - slug: windows-install-iis
    description: "Install IIS using native Windows features instead of Chocolatey"
---
