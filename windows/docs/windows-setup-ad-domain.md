# Setup Active Directory Domain


A workflow that provisions a complete Active Directory environment from scratch in AWS. It creates a keypair, VPC, and three Windows VMs (one domain controller, two domain computers), syncs inventory, tests connectivity, promotes the domain controller, joins the computers to the domain, and validates both PowerShell and Kerberos connectivity. Includes automatic cleanup on failure.

## Workflow

```
Create Keypair ──→ Create VPC ──→ Create DC          ──┐
                              ├──→ Create Computer 1  ──┼──→ Inventory Sync ──→ Test Connectivity
                              └──→ Create Computer 2  ──┘         │
                                                                   ↓
                                                            Create Domain
                                                                   │
                                                            Join Domain ──→ Domain Inventory Sync
                                                                                    │
                                                            ┌───────────────────────┘
                                                            ├──→ PowerShell Validation
                                                            └──→ Kerberos Validation

                                        (any failure) ──→ Cleanup Resources
```

1. **Create Keypair + VPC** — Provisions AWS infrastructure
2. **Create VMs** (parallel) — Deploys one domain controller and two domain computers
3. **Inventory Sync + Test Connectivity** — Verifies all three VMs are reachable
4. **Create Domain** — Promotes the DC to a domain controller
5. **Join Domain** — Joins the two computers to the new domain
6. **Validation** (parallel) — Tests PowerShell and Kerberos authentication

On any failure, the **Cleanup Resources** rollback node runs automatically.

## Prerequisites

- AWS credential configured with Access and Secret key
- SSH public key for AWS keypair creation
- **APD Machine Credential** with Windows administrator credentials
- **AAP Credential** for Controller API callbacks during domain creation

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
| Cloud ǀ AWS ǀ Create Keypair | [`cloud/aws_key.yml`](../../cloud/aws_key.yml) | Creates an SSH keypair in the target AWS region |
| Cloud ǀ AWS ǀ Create VPC | [`cloud/create_vpc.yml`](../../cloud/create_vpc.yml) | Provisions VPC, subnet, security group, and internet gateway |
| Cloud ǀ AWS ǀ Create VM (Domain Controller) | [`cloud/create_vm.yml`](../../cloud/create_vm.yml) | Deploys the dc01 Windows Server instance as domain controller |
| Cloud ǀ AWS ǀ Create VM (Computer 1 - winston) | [`cloud/create_vm.yml`](../../cloud/create_vm.yml) | Deploys the winston Windows Server instance as domain computer |
| Cloud ǀ AWS ǀ Create VM (Computer 2 - winthrop) | [`cloud/create_vm.yml`](../../cloud/create_vm.yml) | Deploys the winthrop Windows Server instance as domain computer |
| AWS Inventory | `(inventory sync)` | Syncs the AWS dynamic inventory to import the new VMs |
| WINDOWS ǀ Test Connectivity | [`windows/connect.yml`](../connect.yml) | Validates WinRM connectivity to all three Windows hosts |
| WINDOWS ǀ AD ǀ Create Domain | [`windows/create_ad_domain.yml`](../create_ad_domain.yml) | Promotes dc01 to domain controller and creates the ANSIBLE.LOCAL domain |
| WINDOWS ǀ AD ǀ Join Domain | [`windows/join_ad_domain.yml`](../join_ad_domain.yml) | Joins winston and winthrop to the Active Directory domain |
| WINDOWS ǀ Run PowerShell (Validation) | [`windows/powershell.yml`](../powershell.yml) | Runs Get-ADComputer on the domain controller to list joined computers |
| WINDOWS ǀ Run PowerShell ǀ Kerberos (Validation) | [`windows/powershell.yml`](../powershell.yml) | Validates Kerberos authentication by querying Security event logs |
| WINDOWS ǀ Rollback (Cleanup) | [`windows/rollback.yml`](../rollback.yml) | Cleans up resources if any workflow step fails |

## Why it matters

- Standing up Active Directory is a multi-step process that teams spend hours on — this workflow does it in one click
- Parallel VM creation demonstrates AAP workflow engine capabilities with dependency management
- Automatic failure handling with resource cleanup shows enterprise-grade error recovery
- Kerberos validation proves end-to-end domain functionality, not just VM provisioning
- The workflow covers infrastructure, configuration, and validation — a complete lifecycle story

## Presenter walkthrough

1. **Set the stage:** Show the empty inventory — no domain hosts exist yet. Explain that the workflow will build everything from scratch.
2. **Walk through the survey:** Fill in the region, owner, environment, subnet, and security group. 'Surveys make this self-service — a helpdesk operator does not need AWS console access.'
3. **Launch and watch parallel creation:** Point out the three VM nodes running simultaneously after VPC creation. 'One domain controller and two member computers, all deploying in parallel.'
4. **Domain promotion:** After connectivity tests pass, the workflow promotes dc01 to a domain controller. 'This is the equivalent of running dcpromo — fully automated.'
5. **Domain join:** Show winston and winthrop joining the domain. 'These machines are now domain members, ready for Group Policy, user management, and Kerberos auth.'
6. **Validation:** Highlight the dual validation — PowerShell queries AD for joined computers, Kerberos checks security event logs. 'We verify the domain actually works, not just that VMs exist.'

## Talking points

- This is a complete infrastructure-to-validation workflow. It provisions VMs, configures Active Directory, and proves it works — all in one click.
- Parallel VM creation with dependency management is a key AAP workflow feature. Three VMs deploy simultaneously, but domain join waits for all three to be ready.
- The automatic cleanup on failure means you never leave orphaned resources in AWS. If domain creation fails, everything rolls back.
- Kerberos validation is the real proof — it shows the domain is functional, not just provisioned.
- After this workflow completes, you can pivot to the Helpdesk New User demo to show AD user management.

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [AD — New User](./windows-ad-new-user.md) | Create users in the domain built by this workflow for a helpdesk self-service demo |
| 🪟 [Patching](./windows-patching.md) | Patch the domain-joined Windows hosts to show day-2 operations |
| 🚀 [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | The general-purpose infrastructure provisioning workflow for mixed OS environments |
