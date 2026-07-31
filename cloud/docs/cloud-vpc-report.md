# AWS — VPC Report


Generates an HTML report of the current AWS VPC infrastructure -- instances, networks, security groups, and tags. Publishes the report to either a Linux report server or an S3 bucket for web access.

## Prerequisites

- AWS credential configured
- Existing infrastructure deployed (e.g., via **Deploy Cloud Stack in AWS**)

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ VPC Report | [`cloud/cloud_report.yml`](../cloud_report.yml) | Gathers facts from EC2 instances and generates an HTML infrastructure report |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](./deploy-cloud-stack.md) | Deploy infrastructure to report on |
