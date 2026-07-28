---
layout: demo-detail
demo_slug: cloud-resize-ec2
description: >-
  Changes the instance type of one or more EC2 instances. Useful for
  demonstrating vertical scaling -- resize a t2.micro to a t2.large and back
  without reprovisioning.
prerequisites:
  - "AWS credential configured"
  - "Running EC2 instances to resize"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Resize EC2"
    playbook: cloud/resize_ec2.yml
    description: "Stops the instance, changes instance type, and restarts it"
related_demos:
  - slug: cloud-snapshot-ec2
    description: "Take a snapshot before resizing as a safety measure"
  - slug: deploy-cloud-stack
    description: "Create instances to resize"
---
