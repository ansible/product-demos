---
layout: demo-detail
demo_slug: cloud-resize-ec2
---

Changes the instance type of one or more EC2 instances. Useful for demonstrating vertical scaling -- resize a t2.micro to a t2.large and back without reprovisioning.

## Prerequisites

- AWS credential configured
- Running EC2 instances to resize

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Resize EC2 | [`cloud/resize_ec2.yml`](https://github.com/ansible/product-demos/blob/main/cloud/resize_ec2.yml) | Stops the instance, changes instance type, and restarts it |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Snapshot EC2](/product-demos/demos/cloud-snapshot-ec2/) | Take a snapshot before resizing as a safety measure |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Create instances to resize |
