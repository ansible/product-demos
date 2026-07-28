---
layout: demo-detail
demo_slug: cloud-create-keypair
description: >-
  Creates an AWS EC2 keypair from the SSH public key attached to the APD
  Machine Credential. If no public key is supplied via survey, the playbook
  derives it automatically from the machine credential private key.
prerequisites:
  - "AWS credential configured"
  - "<strong>APD Machine Credential</strong> with an SSH private key"
job_templates:
  - name: "Cloud | AWS | Create Keypair"
    playbook: cloud/aws_key.yml
    description: "Creates or updates an EC2 keypair, deriving the public key from the machine credential if not provided"
related_demos:
  - slug: deploy-cloud-stack
    description: "Uses this playbook as part of the full stack deployment workflow"
  - slug: cloud-create-vpc
    description: "Create the VPC where you will launch VMs using this keypair"
---
