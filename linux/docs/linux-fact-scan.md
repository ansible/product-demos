---
layout: demo-detail
demo_slug: linux-fact-scan
description: >-
  Scans hosts and gathers package and service facts. This populates the AAP
  fact cache with installed packages and running services, which can then be
  viewed in the host details page. Useful for inventory auditing and
  compliance checks.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "LINUX | Fact Scan"
    playbook: linux/fact_scan.yml
    description: "Gathers package_facts and service_facts, caching them in AAP"
related_demos:
  - slug: linux-troubleshoot
    description: "Active troubleshooting beyond passive fact gathering"
  - slug: deploy-cloud-stack
    description: "Deploy hosts to scan"
---
