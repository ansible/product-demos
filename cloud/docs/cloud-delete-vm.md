---
layout: demo-detail
demo_slug: cloud-delete-vm
description: >-
  Terminates an EC2 instance by its Name tag. Looks up the instance in the
  specified region and terminates it, waiting for the instance to fully shut
  down. Safe to run even if the instance has already been terminated.
prerequisites:
  - "AWS credential configured"
  - "An existing EC2 instance to terminate"
survey_prompts:
  - question: "VM Name"
    variable: create_vm_vm_name
    type: text
    required: "Yes"
  - question: "AWS Region"
    variable: create_vm_aws_region
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Delete VM"
    playbook: cloud/delete_vm_by_name.yml
    description: "Finds and terminates an EC2 instance by its Name tag"
related_demos:
  - slug: cloud-create-vm
    description: "Create VMs that can be cleaned up with this playbook"
  - slug: cloud-destroy-stack
    description: "Tear down the entire demo stack at once"
---
