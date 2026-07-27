---
layout: demo-detail
demo_slug: windows-setup-ad-domain
prerequisites:
  - "AWS credential configured with Access and Secret key"
  - "SSH public key for AWS keypair creation"
  - "<strong>APD Machine Credential</strong> with Windows administrator credentials"
  - "<strong>AAP Credential</strong> for Controller API callbacks during domain creation"
survey_prompts:
  - question: "AWS Region"
    variable: create_vm_aws_region
    type: multiplechoice
    required: "Yes"
  - question: "Keypair Public Key"
    variable: aws_public_key
    type: textarea
    required: "Yes"
  - question: "Owner"
    variable: create_vm_vm_owner
    type: text
    required: "Yes"
  - question: "Environment"
    variable: create_vm_vm_environment
    type: multiplechoice
    required: "Yes"
  - question: "Subnet"
    variable: create_vm_aws_vpc_subnet_name
    type: text
    required: "Yes"
  - question: "Security Group"
    variable: create_vm_aws_securitygroup_name
    type: text
    required: "Yes"
job_templates:
  - name: "Cloud | AWS | Create Keypair"
    playbook: cloud/create_keypair.yml
    description: "Creates an SSH keypair in the target AWS region"
  - name: "Cloud | AWS | Create VPC"
    playbook: cloud/create_vpc.yml
    description: "Provisions VPC, subnet, security group, and internet gateway"
  - name: "Cloud | AWS | Create VM (Domain Controller)"
    playbook: cloud/create_vm.yml
    description: "Deploys the dc01 Windows Server instance as domain controller"
  - name: "Cloud | AWS | Create VM (Computer 1 - winston)"
    playbook: cloud/create_vm.yml
    description: "Deploys the winston Windows Server instance as domain computer"
  - name: "Cloud | AWS | Create VM (Computer 2 - winthrop)"
    playbook: cloud/create_vm.yml
    description: "Deploys the winthrop Windows Server instance as domain computer"
  - name: "AWS Inventory"
    playbook: (inventory sync)
    description: "Syncs the AWS dynamic inventory to import the new VMs"
  - name: "WINDOWS | Test Connectivity"
    playbook: windows/connect.yml
    description: "Validates WinRM connectivity to all three Windows hosts"
  - name: "WINDOWS | AD | Create Domain"
    playbook: windows/create_ad_domain.yml
    description: "Promotes dc01 to domain controller and creates the ANSIBLE.LOCAL domain"
  - name: "WINDOWS | AD | Join Domain"
    playbook: windows/join_ad_domain.yml
    description: "Joins winston and winthrop to the Active Directory domain"
  - name: "WINDOWS | Run PowerShell (Validation)"
    playbook: windows/powershell.yml
    description: "Runs Get-ADComputer on the domain controller to list joined computers"
  - name: "WINDOWS | Run PowerShell | Kerberos (Validation)"
    playbook: windows/powershell.yml
    description: "Validates Kerberos authentication by querying Security event logs"
  - name: "WINDOWS | Rollback (Cleanup)"
    playbook: windows/rollback.yml
    description: "Cleans up resources if any workflow step fails"
related_demos:
  - slug: windows-ad-new-user
    description: "Create users in the domain built by this workflow for a helpdesk self-service demo"
  - slug: windows-patching
    description: "Patch the domain-joined Windows hosts to show day-2 operations"
  - slug: deploy-cloud-stack
    description: "The general-purpose infrastructure provisioning workflow for mixed OS environments"
---

A workflow that provisions a complete Active Directory environment from scratch in AWS. It creates a keypair, VPC, and three Windows VMs (one domain controller, two domain computers), syncs inventory, tests connectivity, promotes the domain controller, joins the computers to the domain, and validates both PowerShell and Kerberos connectivity. Includes automatic cleanup on failure.

_One-click Active Directory domain with infrastructure, domain join, and Kerberos validation_

## Why it matters

- Standing up Active Directory is a multi-step process that teams spend hours on — this workflow does it in one click
- Parallel VM creation demonstrates AAP workflow engine capabilities with dependency management
- Automatic failure handling with resource cleanup shows enterprise-grade error recovery
- Kerberos validation proves end-to-end domain functionality, not just VM provisioning
- The workflow covers infrastructure, configuration, and validation — a complete lifecycle story

## Presenter walkthrough

1. <strong>Set the stage:</strong> Show the empty inventory — no domain hosts exist yet. Explain that the workflow will build everything from scratch.
2. <strong>Walk through the survey:</strong> Fill in the region, owner, environment, subnet, and security group. 'Surveys make this self-service — a helpdesk operator does not need AWS console access.'
3. <strong>Launch and watch parallel creation:</strong> Point out the three VM nodes running simultaneously after VPC creation. 'One domain controller and two member computers, all deploying in parallel.'
4. <strong>Domain promotion:</strong> After connectivity tests pass, the workflow promotes dc01 to a domain controller. 'This is the equivalent of running dcpromo — fully automated.'
5. <strong>Domain join:</strong> Show winston and winthrop joining the domain. 'These machines are now domain members, ready for Group Policy, user management, and Kerberos auth.'
6. <strong>Validation:</strong> Highlight the dual validation — PowerShell queries AD for joined computers, Kerberos checks security event logs. 'We verify the domain actually works, not just that VMs exist.'

## Talking points

- This is a complete infrastructure-to-validation workflow. It provisions VMs, configures Active Directory, and proves it works — all in one click.
- Parallel VM creation with dependency management is a key AAP workflow feature. Three VMs deploy simultaneously, but domain join waits for all three to be ready.
- The automatic cleanup on failure means you never leave orphaned resources in AWS. If domain creation fails, everything rolls back.
- Kerberos validation is the real proof — it shows the domain is functional, not just provisioned.
- After this workflow completes, you can pivot to the Helpdesk New User demo to show AD user management.
