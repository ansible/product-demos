---
layout: demo-detail
demo_slug: cloud-create-vpc
prerequisites:
  - "AWS credential configured with Access and Secret key"
  - "Run <strong>APD | Single demo setup</strong> with <code>cloud</code> to create the job template"
job_templates:
  - name: "Cloud | AWS | Create VPC"
    playbook: cloud/create_vpc.yml
    description: "Provisions VPC, subnet, security group, internet gateway, and route table in the selected region"
related_demos:
  - slug: deploy-cloud-stack
    description: "Uses this playbook as part of the full stack deployment workflow"
  - slug: cloud-create-keypair
    description: "Create an SSH keypair to use with VMs in this VPC"
---

Provisions an AWS VPC with subnet, internet gateway, route table, and security group. Supports multiple regions with configurable availability zones. This is a building-block playbook used by the Deploy Cloud Stack workflow and can also be run standalone.

_Create a full VPC with networking in one playbook_
