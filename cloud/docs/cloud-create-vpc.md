---
layout: demo-detail
demo_slug: cloud-create-vpc
---

Provisions an AWS VPC with subnet, internet gateway, route table, and security group. Supports multiple regions with configurable availability zones. This is a building-block playbook used by the Deploy Cloud Stack workflow and can also be run standalone.

## Prerequisites

- AWS credential configured with Access and Secret key
- Run <strong>APD | Single demo setup</strong> with <code>cloud</code> to create the job template

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud | AWS | Create VPC | [`cloud/create_vpc.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_vpc.yml) | Provisions VPC, subnet, security group, internet gateway, and route table in the selected region |

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Uses this playbook as part of the full stack deployment workflow |
| ☁️ [AWS — Create Keypair](/product-demos/demos/cloud-create-keypair/) | Create an SSH keypair to use with VMs in this VPC |
