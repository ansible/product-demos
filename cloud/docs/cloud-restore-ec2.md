---
layout: demo-detail
demo_slug: cloud-restore-ec2
---

Restores EC2 instance volumes from the most recent EBS snapshot. This is the rollback mechanism used by the patching workflow -- if patching fails, instances are restored to the pre-patch state.

## Prerequisites

- AWS credential configured
- A previous snapshot taken with <strong>Cloud | AWS | Snapshot EC2</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud | AWS | Restore EC2 from Snapshot | [`cloud/restore_ec2.yml`](https://github.com/ansible/product-demos/blob/main/cloud/restore_ec2.yml) | Restores volumes from the latest EBS snapshot for the target instances |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Snapshot EC2](/product-demos/demos/cloud-snapshot-ec2/) | Take snapshots before making changes |
| 🩹 [Patch Cloud Stack in AWS](/product-demos/demos/patch-cloud-stack/) | The patching workflow automates snapshot/restore on failure |
