# AWS — Create VPC


Provisions an AWS VPC with subnet, internet gateway, route table, and security group. Supports multiple regions with configurable availability zones. This is a building-block playbook used by the Deploy Cloud Stack workflow and can also be run standalone.

## Prerequisites

- AWS credential configured with Access and Secret key
- Run **APD ǀ Single demo setup** with `cloud` to create the job template

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create VPC | [`cloud/create_vpc.yml`](../create_vpc.yml) | Provisions VPC, subnet, security group, internet gateway, and route table in the selected region |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](./deploy-cloud-stack.md) | Uses this playbook as part of the full stack deployment workflow |
| ☁️ [AWS — Create Keypair](./cloud-create-keypair.md) | Create an SSH keypair to use with VMs in this VPC |
