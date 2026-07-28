---
layout: demo-detail
demo_slug: linux-temporary-sudo
description: >-
  Grants temporary sudo access to a user for a configurable duration. Creates
  a sudoers rule, schedules automatic cleanup via the at daemon, and removes
  the rule when time expires. Demonstrates just-in-time privilege escalation.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
  - "The target user must exist on the system"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Sudo User"
    variable: sudo_user
    type: text
    required: "Yes"
  - question: "Time"
    variable: sudo_time
    type: integer
    required: "Yes"
  - question: "Time Units"
    variable: sudo_units
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "LINUX | Temporary Sudo"
    playbook: linux/temp_sudo.yml
    description: "Creates a time-limited sudoers rule and schedules automatic cleanup"
related_demos:
  - slug: linux-run-shell-script
    description: "Run scripts that may need the temporary privileges"
---
