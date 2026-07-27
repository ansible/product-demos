---
layout: demo-detail
demo_slug: linux-deploy-application
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Application"
    variable: application
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Deploy Application"
    playbook: linux/deploy_application.yml
    description: "Installs or updates an application package via DNF on target hosts"
related_demos:
  - slug: linux-podman-webserver
    description: "Container-based deployment as an alternative to packages"
---

Installs a Linux application package via DNF. Supports version pinning with allow_downgrade for rollback scenarios. A straightforward demo of application deployment that shows how AAP replaces manual package management.

_Install or roll back a Linux application package_
