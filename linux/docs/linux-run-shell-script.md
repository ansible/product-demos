---
layout: demo-detail
demo_slug: linux-run-shell-script
description: >-
  Runs an arbitrary shell script on target hosts. The script content is
  provided via survey. Outputs the result and reminds users they should
  consider converting scripts to proper playbooks. Great for showing the
  migration path from scripts to automation.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Shell Script"
    variable: shell_script
    type: textarea
    required: "Yes"
job_templates:
  - name: "LINUX | Run Shell Script"
    playbook: linux/run_script.yml
    description: "Executes the provided shell script on target hosts and displays the output"
related_demos:
  - slug: linux-troubleshoot
    description: "Pre-built troubleshooting commands instead of ad-hoc scripts"
---
