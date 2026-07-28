---
layout: demo-detail
demo_slug: linux-start-service
description: >-
  Starts a named systemd service on target hosts. Checks that the service
  exists before attempting to start it. A simple but common operational task
  that demonstrates self-service IT operations.
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
  - name: "LINUX | Start Service"
    playbook: linux/service_start.yml
    description: "Checks for the service and starts it if present"
related_demos:
  - slug: linux-stop-service
    description: "Stop a running service"
---
