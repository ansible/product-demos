---
layout: demo-detail
demo_slug: cloud-vpc-report
---

Generates an HTML report of the current AWS VPC infrastructure -- instances, networks, security groups, and tags. Publishes the report to either a Linux report server or an S3 bucket for web access.

## Prerequisites

- AWS credential configured
- Existing infrastructure deployed (e.g., via <strong>Deploy Cloud Stack in AWS</strong>)

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud | AWS | VPC Report | [`cloud/cloud_report.yml`](https://github.com/ansible/product-demos/blob/main/cloud/cloud_report.yml) | Gathers facts from EC2 instances and generates an HTML infrastructure report |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Deploy infrastructure to report on |
