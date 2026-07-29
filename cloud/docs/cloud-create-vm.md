# AWS — Create VM


Launches an EC2 instance from a blueprint definition. Blueprints are YAML files under cloud/blueprints/ that define AMI, instance type, security group, tags, and user data. Supports both Linux and Windows instances with automatic WinRM bootstrapping for Windows.

## Prerequisites

- AWS credential configured
- A VPC, subnet, security group, and keypair already created
- A blueprint file under <code>cloud/blueprints/</code>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `create_vm_aws_region` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create VM | [`cloud/create_vm.yml`](../create_vm.yml) | Provisions an EC2 instance using a blueprint, sets tags, and waits for connectivity |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](./deploy-cloud-stack.md) | Launches multiple VMs in parallel using this playbook |
| ☁️ [AWS — Delete VM](./cloud-delete-vm.md) | Terminate VMs created by this playbook |
