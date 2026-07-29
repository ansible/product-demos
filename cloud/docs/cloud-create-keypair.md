# AWS — Create Keypair


Creates an AWS EC2 keypair from the SSH public key attached to the APD Machine Credential. If no public key is supplied via survey, the playbook derives it automatically from the machine credential private key.

## Prerequisites

- AWS credential configured
- **APD Machine Credential** with an SSH private key

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create Keypair | [`cloud/aws_key.yml`](../aws_key.yml) | Creates or updates an EC2 keypair, deriving the public key from the machine credential if not provided |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](./deploy-cloud-stack.md) | Uses this playbook as part of the full stack deployment workflow |
| ☁️ [AWS — Create VPC](./cloud-create-vpc.md) | Create the VPC where you will launch VMs using this keypair |
