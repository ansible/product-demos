# Setup Active Directory Domain


A workflow that provisions a complete Active Directory environment from scratch in AWS. It creates a keypair, VPC, and three Windows VMs (one domain controller, two domain computers), syncs inventory, tests connectivity, promotes the domain controller, joins the computers to the domain, and validates both PowerShell and Kerberos connectivity. Includes automatic cleanup on failure.

## Prerequisites

- AWS credential configured with Access and Secret key
- SSH public key for AWS keypair creation
- <strong>APD Machine Credential</strong> with Windows administrator credentials
- <strong>AAP Credential</strong> for Controller API callbacks during domain creation

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `create_vm_aws_region` | multiplechoice | Yes |
| Keypair Public Key | `aws_public_key` | textarea | Yes |
| Owner | `create_vm_vm_owner` | text | Yes |
| Environment | `create_vm_vm_environment` | multiplechoice | Yes |
| Subnet | `create_vm_aws_vpc_subnet_name` | text | Yes |
| Security Group | `create_vm_aws_securitygroup_name` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create Keypair | [`cloud/create_keypair.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_keypair.yml) | Creates an SSH keypair in the target AWS region |
| Cloud ǀ AWS ǀ Create VPC | [`cloud/create_vpc.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_vpc.yml) | Provisions VPC, subnet, security group, and internet gateway |
| Cloud ǀ AWS ǀ Create VM (Domain Controller) | [`cloud/create_vm.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_vm.yml) | Deploys the dc01 Windows Server instance as domain controller |
| Cloud ǀ AWS ǀ Create VM (Computer 1 - winston) | [`cloud/create_vm.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_vm.yml) | Deploys the winston Windows Server instance as domain computer |
| Cloud ǀ AWS ǀ Create VM (Computer 2 - winthrop) | [`cloud/create_vm.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_vm.yml) | Deploys the winthrop Windows Server instance as domain computer |
| AWS Inventory | [`(inventory sync)`](https://github.com/ansible/product-demos/blob/main/(inventory sync)) | Syncs the AWS dynamic inventory to import the new VMs |
| WINDOWS ǀ Test Connectivity | [`windows/connect.yml`](https://github.com/ansible/product-demos/blob/main/windows/connect.yml) | Validates WinRM connectivity to all three Windows hosts |
| WINDOWS ǀ AD ǀ Create Domain | [`windows/create_ad_domain.yml`](https://github.com/ansible/product-demos/blob/main/windows/create_ad_domain.yml) | Promotes dc01 to domain controller and creates the ANSIBLE.LOCAL domain |
| WINDOWS ǀ AD ǀ Join Domain | [`windows/join_ad_domain.yml`](https://github.com/ansible/product-demos/blob/main/windows/join_ad_domain.yml) | Joins winston and winthrop to the Active Directory domain |
| WINDOWS ǀ Run PowerShell (Validation) | [`windows/powershell.yml`](https://github.com/ansible/product-demos/blob/main/windows/powershell.yml) | Runs Get-ADComputer on the domain controller to list joined computers |
| WINDOWS ǀ Run PowerShell ǀ Kerberos (Validation) | [`windows/powershell.yml`](https://github.com/ansible/product-demos/blob/main/windows/powershell.yml) | Validates Kerberos authentication by querying Security event logs |
| WINDOWS ǀ Rollback (Cleanup) | [`windows/rollback.yml`](https://github.com/ansible/product-demos/blob/main/windows/rollback.yml) | Cleans up resources if any workflow step fails |

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

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [AD — New User](/product-demos/demos/windows-ad-new-user/) | Create users in the domain built by this workflow for a helpdesk self-service demo |
| 🪟 [Patching](/product-demos/demos/windows-patching/) | Patch the domain-joined Windows hosts to show day-2 operations |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | The general-purpose infrastructure provisioning workflow for mixed OS environments |
