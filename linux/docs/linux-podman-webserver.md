---
layout: demo-detail
demo_slug: linux-podman-webserver
description: >-
  Deploys a containerized Apache httpd webserver using Podman. Installs
  Podman, creates a volume directory with a custom index.html, and runs an
  httpd container serving the custom page. Demonstrates rootless container
  management with Ansible.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Web Page Message"
    variable: message
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Podman Webserver"
    playbook: linux/podman.yml
    description: "Installs Podman, creates a custom index.html, and runs an httpd container"
related_demos:
  - slug: linux-deploy-application
    description: "Traditional package-based application deployment"
---
