---
layout: demo-detail
demo_slug: cloud-snapshot-ec2
description: >-
  Creates EBS snapshots of all volumes attached to the target EC2 instances.
  Used as a safety net before patching or other changes -- if something goes
  wrong, you can restore from these snapshots.
prerequisites:
  - "AWS credential configured"
  - "Running EC2 instances to snapshot"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Snapshot EC2"
    playbook: cloud/snapshot_ec2.yml
    description: "Creates EBS snapshots of all volumes on the target instances"
related_demos:
  - slug: cloud-restore-ec2
    description: "Restore instances from snapshots created by this playbook"
  - slug: patch-cloud-stack
    description: "The patching workflow uses snapshots as its safety net"
---
