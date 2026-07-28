---
layout: demo-detail
demo_slug: cloud-restore-ec2
description: >-
  Restores EC2 instance volumes from the most recent EBS snapshot. This is the
  rollback mechanism used by the patching workflow -- if patching fails,
  instances are restored to the pre-patch state.
prerequisites:
  - "AWS credential configured"
  - "A previous snapshot taken with <strong>Cloud | AWS | Snapshot EC2</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Restore EC2 from Snapshot"
    playbook: cloud/restore_ec2.yml
    description: "Restores volumes from the latest EBS snapshot for the target instances"
related_demos:
  - slug: cloud-snapshot-ec2
    description: "Take snapshots before making changes"
  - slug: patch-cloud-stack
    description: "The patching workflow automates snapshot/restore on failure"
---
