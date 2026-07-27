---
layout: demo-detail
demo_slug: cloud-create-vm
prerequisites:
  - "AWS credential configured"
  - "A VPC, subnet, security group, and keypair already created"
  - "A blueprint file under <code>cloud/blueprints/</code>"
survey_prompts:
  - question: "AWS Region"
    variable: create_vm_aws_region
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Create VM"
    playbook: cloud/create_vm.yml
    description: "Provisions an EC2 instance using a blueprint, sets tags, and waits for connectivity"
related_demos:
  - slug: deploy-cloud-stack
    description: "Launches multiple VMs in parallel using this playbook"
  - slug: cloud-delete-vm
    description: "Terminate VMs created by this playbook"
---

Launches an EC2 instance from a blueprint definition. Blueprints are YAML files under cloud/blueprints/ that define AMI, instance type, security group, tags, and user data. Supports both Linux and Windows instances with automatic WinRM bootstrapping for Windows.

_Launch an EC2 instance from a reusable blueprint_
