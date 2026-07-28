---
layout: demo-detail
demo_slug: linux-stop-service
description: >-
  Stops a named systemd service on target hosts. Checks that the service
  exists before attempting to stop it. Paired with Start Service for basic
  service lifecycle management.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Service Name"
    variable: service_name
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Stop Service"
    playbook: linux/service_stop.yml
    description: "Checks for the service and stops it if present"
related_demos:
  - slug: linux-start-service
    description: "Start a stopped service"
---
