# AWS — Restore EC2 from Snapshot


Restores EC2 instance volumes from the most recent EBS snapshot. This is the rollback mechanism used by the patching workflow -- if patching fails, instances are restored to the pre-patch state.

## Prerequisites

- AWS credential configured
- A previous snapshot taken with **Cloud ǀ AWS ǀ Snapshot EC2**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| AWS Region | `aws_region` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Restore EC2 from Snapshot | [`cloud/restore_ec2.yml`](../restore_ec2.yml) | Restores volumes from the latest EBS snapshot for the target instances |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Snapshot EC2](./cloud-snapshot-ec2.md) | Take snapshots before making changes |
| 🩹 [Patch Cloud Stack in AWS](./patch-cloud-stack.md) | The patching workflow automates snapshot/restore on failure |
