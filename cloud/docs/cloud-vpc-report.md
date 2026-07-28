---
layout: demo-detail
demo_slug: cloud-vpc-report
description: >-
  Generates an HTML report of the current AWS VPC infrastructure -- instances,
  networks, security groups, and tags. Publishes the report to either a Linux
  report server or an S3 bucket for web access.
prerequisites:
  - "AWS credential configured"
  - "Existing infrastructure deployed (e.g., via <strong>Deploy Cloud Stack in AWS</strong>)"
job_templates:
  - name: "Cloud | AWS | VPC Report"
    playbook: cloud/cloud_report.yml
    description: "Gathers facts from EC2 instances and generates an HTML infrastructure report"
related_demos:
  - slug: deploy-cloud-stack
    description: "Deploy infrastructure to report on"
---
