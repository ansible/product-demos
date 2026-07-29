# AWS — Snapshot EC2


Creates EBS snapshots of all volumes attached to the target EC2 instances. Used as a safety net before patching or other changes -- if something goes wrong, you can restore from these snapshots.

## Prerequisites

- AWS credential configured
- Running EC2 instances to snapshot

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| AWS Region | `aws_region` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Snapshot EC2 | [`cloud/snapshot_ec2.yml`](../snapshot_ec2.yml) | Creates EBS snapshots of all volumes on the target instances |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Restore EC2 from Snapshot](./cloud-restore-ec2.md) | Restore instances from snapshots created by this playbook |
| 🩹 [Patch Cloud Stack in AWS](./patch-cloud-stack.md) | The patching workflow uses snapshots as its safety net |
