---
layout: demo-detail
demo_slug: cloud-delete-vm
---

Terminates an EC2 instance by its Name tag. Looks up the instance in the specified region and terminates it, waiting for the instance to fully shut down. Safe to run even if the instance has already been terminated.

## Prerequisites

- AWS credential configured
- An existing EC2 instance to terminate

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| VM Name | `create_vm_vm_name` | text | Yes |
| AWS Region | `create_vm_aws_region` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud | AWS | Delete VM | [`cloud/delete_vm_by_name.yml`](https://github.com/ansible/product-demos/blob/main/cloud/delete_vm_by_name.yml) | Finds and terminates an EC2 instance by its Name tag |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Create VM](/product-demos/demos/cloud-create-vm/) | Create VMs that can be cleaned up with this playbook |
| 💥 [Destroy Cloud Stack in AWS](/product-demos/demos/cloud-destroy-stack/) | Tear down the entire demo stack at once |
