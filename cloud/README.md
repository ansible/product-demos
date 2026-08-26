# Cloud Demos

## Table of Contents
- [Cloud Demos](#cloud-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
    - [Workflows](#workflows)
    - [Inventory](#inventory)
  - [Post Setup Setup](#post-setup-setup)
    - [Configure Credentials](#configure-credentials)
    - [Configure APD Machine Credential SSH Key](#configure-apd-machine-credential-ssh-key)
  - [Suggested Usage](#suggested-usage)
  - [Known Issues](#known-issues)

## About These Demos
This category of demos shows examples of multi-cloud provisioning and management with Ansible Automation Platform. The list of demos can be found below. These demos are particularly helpful in building additional infrastructure for other demo categories such as Linux and Windows. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Workflows

| Workflow | Description |
|----------|-------------|
| [**Patch Cloud Stack in AWS**](docs/patch-cloud-stack.md) | Enterprise-grade patching workflow with EBS snapshots, parallel RHEL and Windows paths, automatic rollback on failure, and a consolidated compliance report. |
| [**Deploy Cloud Stack in AWS**](docs/deploy-cloud-stack.md) | One-click workflow to provision a full demo stack — VPC, keypair, and five VMs (2 Windows, 2 RHEL, 1 report server) — with inventory sync and VPC report. |
| [**Destroy Cloud Stack in AWS**](docs/cloud-destroy-stack.md) | Tear down all five stack VMs, VPC, and keypair created by Deploy Cloud Stack, then sync inventory. |

### Jobs

| Job Template | Description |
|--------------|-------------|
| [**AWS — Create VPC**](docs/cloud-create-vpc.md) | Create an AWS VPC with subnet, security group, and route table in a selected region. |
| [**AWS — Create Keypair**](docs/cloud-create-keypair.md) | Create an AWS EC2 keypair, deriving the public key from the APD Machine Credential's private key. |
| [**AWS — Create VM**](docs/cloud-create-vm.md) | Create an EC2 instance from a blueprint (RHEL 7/8/9, Windows Core/Full, AL2023) with full tagging support. |
| [**AWS — Delete VM**](docs/cloud-delete-vm.md) | Terminate an EC2 instance by Name tag and region. |
| [**AWS — Resize EC2**](docs/cloud-resize-ec2.md) | Change the instance type of a running EC2 instance and refresh the AWS inventory. |
| [**AWS — Snapshot EC2**](docs/cloud-snapshot-ec2.md) | Create EBS snapshots of EC2 instances for backup and recovery. |
| [**AWS — Restore EC2 from Snapshot**](docs/cloud-restore-ec2.md) | Restore EC2 instance volumes from their latest EBS snapshot. |
| [**AWS — Peer Networking**](docs/cloud-peer-networking.md) | Create or delete VPC peering infrastructure in AWS for direct network connectivity between VPCs. |
| [**AWS — Transit Networking**](docs/cloud-transit-networking.md) | Create or delete transit gateway infrastructure in AWS for hub-and-spoke network connectivity. |
| [**AWS — VPC Report**](docs/cloud-vpc-report.md) | Generate a VPC infrastructure report and publish it to an S3 bucket. |

## Post Setup Setup
After running the setup job template, there are a few steps required to make the demos fully functional. See post setup actions below.

   > These steps may differ if you in your environment

### Configure Credentials

- Add AWS Access and Secret key to the `AWS` Credential created by the setup job.

### Configure APD Machine Credential SSH Key

The **APD Machine Credential** is used for both Windows and Linux instances: the username and password are used for Windows connections (WinRM), and the SSH private key is used for Linux connections.

For **Deploy Cloud Stack in AWS**, add an **SSH private key** to **APD Machine Credential**. The **Create Keypair** job derives the matching public key automatically (`ssh-keygen -y`); no public key survey field is required.

Linux jobs such as **Linux | Fact Scan** will fail with `Permission denied (publickey)` until a private key is saved on this credential.

When bootstrapping AAP manually, you can pre-load the SSH key with the `vault_apd_machine_credential_ssh_key` extra var (see `common/bootstrap-vars.yml`).

For standalone runs of **Cloud / AWS | Create Keypair**, paste a public key in the optional survey field only if **APD Machine Credential** does not include a private key.

## Suggested Usage

### Deploy Cloud Stack in AWS

This is the typical starting point for cloud demos in AWS. Launch the workflow and complete the survey:

| Prompt | Purpose |
|--------|---------|
| **AWS Region** | Region for all stack resources |
| **Owner** | Tag value for owner on VPC, keypair, and VMs |
| **Environment** | Dev / QA / Prod tag on VMs |
| **Email** | Used by feedback/telemetry jobs |

The workflow:

1. Creates keypair `aws-test-key` (public key derived from **APD Machine Credential** private key)
2. Creates VPC `aws-test-vpc` with subnet, security group, and route table
3. Deploys five VMs **in parallel**:
   | VM name | Blueprint |
   |---------|-----------|
   | `aws-dc` | windows_full |
   | `aws_win1` | windows_core |
   | `aws_rhel8` | rhel8 |
   | `aws_rhel9` | rhel9 |
   | `reports` | rhel9 |
4. Syncs AWS inventory and publishes the VPC report to S3

Preset tags: deployment `cloud_stack`, purpose `demo`. Owner and environment come from the survey.

**Prerequisites:** AWS credential configured and an SSH private key on **APD Machine Credential**.

### Destroy Cloud Stack in AWS

Use this workflow to completely tear down a stack created by **Deploy Cloud Stack in AWS** and start fresh. Launch it and select the **same AWS Region** used for deploy — that is the only survey prompt.

The workflow:

1. Terminates all five stack VMs **in parallel** (`aws-dc`, `aws_win1`, `aws_rhel8`, `aws_rhel9`, `reports`)
2. Deletes VPC `aws-test-vpc` and related resources (subnet, route table, internet gateway, security group)
3. Deletes keypair `aws-test-key` (runs in parallel with VPC teardown)
4. Syncs AWS inventory so hosts are removed from AAP

**Note:** S3 report buckets created during deploy (`reports-pd-*`) are not deleted by this workflow.

### Patch Cloud Stack in AWS

This workflow demonstrates enterprise-grade patching with snapshot safety, parallel RHEL/Windows paths, automatic rollback on failure, and a consolidated compliance report. It is designed to run against the VMs deployed by **Deploy Cloud Stack in AWS** and covers both operating systems in a single execution. Based on [jopaik/patch_demo](https://github.com/jopaik/patch_demo).

Launch the workflow and complete the survey:

| Prompt | Purpose |
|--------|---------|
| **AWS Region** | Region where the stack is deployed |
| **RHEL hosts** | Host pattern for RHEL nodes (default `aws_rhel*`; does not match `reports` or `aws_kafka`) |
| **Windows hosts** | Host pattern for Windows nodes (default `aws_win*`; does not match `aws-dc`) |
| **RHEL Advisory IDs** | Comma-separated RHSA/CVE IDs to patch (e.g. `RHSA-2024:3138, CVE-2024-33599`) |
| **Windows KB IDs** | Comma-separated KB IDs to patch (e.g. `KB5044284, KB5044030`) |

The workflow:

```
Take Snapshot
├─→ Pre-check RHEL ─→ Patch RHEL
│       ├─ (success) Post-check RHEL ──→ (always) ──┐
│       └─ (fail)    Restore RHEL from Snapshot      │
├─→ Pre-check Windows ─→ Patch Windows              │
│       ├─ (success) Post-check Windows ─→ (always) ─┤
│       └─ (fail)    Restore Windows from Snapshot    │
└──────────────────────────────────────────────────── ALL → Compliance Report
```

1. **Take Snapshot** — EBS snapshots of all target instances for recovery
2. **Pre-check** (parallel) — Queries advisory/KB applicability on RHEL and Windows
3. **Patch** (parallel) — Applies targeted advisories via `dnf` (RHEL) or `win_updates` (Windows)
4. **Post-check / Restore** — Verifies compliance; on failure restores from the EBS snapshot taken in step 1
5. **Compliance Report** — Generates an HTML dashboard at `http://<reports>/patch_report.html` (runs only when at least one post-check completes)

**Prerequisites:**
- Run **Deploy Cloud Stack in AWS** first to create the target VMs
- AWS credential configured
- SSH private key on **APD Machine Credential**

> **Note:** This workflow replaces the older *Cloud / AWS / Patch EC2 Workflow* and adds Windows support, pre/post verification, and snapshot-based restore on failure. The rollback job templates (`Cloud | AWS | Patch Rollback RHEL` / `Windows`) are also available as standalone jobs for undoing patches without a full snapshot restore. See also [Linux / Patching](../linux/README.md) and [Windows / Patching](../windows/README.md) for standalone OS-specific patching jobs.

### Other jobs

**Cloud / Create VM** - The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM [blueprints](blueprints/) define variables for each provider that override the defaults in the collection. When creating VMs it is recommended to follow naming conventions that can be used as host patterns. (eg. VM names: `win1`, `win2`, `win3`.  Host Pattern: `win*` )

**Cloud / AWS / Resize EC2** - Given an EC2 instance, change its size. This takes an AWS region, target host pattern, and a target instance size as parameters. As a final step, this job refreshes the AWS inventory so the re-created instance is accessible from AAP.

## Known Issues

- Azure does not work without a custom execution environment that includes the Azure dependencies.
