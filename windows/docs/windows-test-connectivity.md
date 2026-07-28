---
layout: demo-detail
demo_slug: windows-test-connectivity
description: >-
  Tests WinRM connectivity to Windows hosts using wait_for_connection and
  win_ping. Verifies that AAP can reach the hosts before running any
  configuration. Useful as a smoke test after provisioning.
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "WINDOWS | Test Connectivity"
    playbook: windows/connect.yml
    description: "Waits for WinRM to become available and runs win_ping to confirm connectivity"
related_demos:
  - slug: windows-install-iis
    description: "Run a quick demo after confirming connectivity"
  - slug: deploy-cloud-stack
    description: "Deploy Windows VMs to test against"
---
