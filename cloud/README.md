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

### Jobs

- [**Cloud / AWS / Create VM**](create_vm.yml) - Create a VM based on a [blueprint](blueprints/) in the selected cloud provider
- [**Cloud / AWS / Destroy VM**](destroy_vm.yml) - Destroy a VM that has been created in a cloud provider. VM must be imported into dynamic inventory to be deleted.
- [**Cloud / AWS / Snapshot EC2**](snapshot_ec2.yml) - Snapshot a VM that has been created in a cloud provider. VM must be imported into dynamic inventory to be snapshot.
- [**Cloud / AWS / Restore EC2 from Snapshot**](snapshot_ec2.yml) - Restore a VM that has been created in a cloud provider.  By default, volumes will be restored from their latest snapshot. VM must be imported into dynamic inventory to be patched.
- [**Cloud / Resize EC2**](resize_ec2.yml) - Re-size an EC2 instance.

### Workflows

- **Deploy Cloud Stack in AWS** - Provisions the full demo stack (VPC, keypair, five VMs, reports). See [Suggested Usage](#suggested-usage).
- **Destroy Cloud Stack in AWS** - Tears down everything created by Deploy Cloud Stack in AWS. See [Suggested Usage](#suggested-usage).
- **Cloud / AWS / Patch EC2 Workflow** - Snapshot, patch, and optionally restore Linux instances.

### Inventory

A dynamic inventory is created to pull inventory hosts from cloud providers. The VM will be added by name therefore provisioning VMs with the same name will cause conflict in the inventory.

Groups will be created based on the operating system (platform) of the VM provisioned as well as a group called `cloud_<cloud provider>`.

## Post Setup Setup
After running the setup job template, there are a few steps required to make the demos fully functional. See post setup actions below.

   > These steps may differ if you in your environment

### Configure Credentials

- Add AWS Access and Secret key to the `AWS` Credential created by the setup job.

### Configure APD Machine Credential SSH Key

The **APD Machine Credential** is created at install with username `ec2-user` and demo password `Admin_1234!` (Windows complexity compliant). That password is used when Windows instances are provisioned and for WinRM jobs against `ec2-user`.

For **Deploy Cloud Stack in AWS**, add the **private SSH key** (RSA or ECDSA, not ED25519) to **APD Machine Credential** — the same private key you use to SSH to the RHDP bastion. The **Create Keypair** job derives the matching public key automatically (`ssh-keygen -y`); you do **not** need to copy the public key from the demo portal into the workflow survey.

On **demo.redhat.com**, the catalog page shows a public key under **Bastion Host Credentials** for reference and for SSH to the bastion itself. That public key pairs with the private key you save on **APD Machine Credential**. One-time setup: paste the private key on the credential, then every deploy reuses it.

Linux jobs such as **Linux | Fact Scan** will fail with `Permission denied (publickey)` until the matching private key is saved on this credential.

Install-time pre-configuration (optional, for RHDP operators): set `vault_apd_machine_credential_ssh_key` in bootstrap extra vars so the bastion private key is loaded when AAP is provisioned and users never touch credentials manually.

Override the defaults at install time with extra vars if needed:

- `apd_machine_credential_user`
- `apd_machine_credential_password` or `vault_apd_machine_credential_password`
- `vault_apd_machine_credential_ssh_key`

### Getting your SSH key for Create Keypair

When launching **Deploy Cloud Stack in AWS**, no public key survey field is required — **Create Keypair** reads the private key from **APD Machine Credential** and registers the derived public key in AWS.

For standalone runs of **Cloud / AWS | Create Keypair**, paste a public key in the optional survey field only if **APD Machine Credential** does not include a private key.

**Important:** Do not use **ED25519** keys (`ssh-ed25519`). AWS does not support ED25519 key pairs with Windows AMIs, and the Deploy Cloud Stack workflow provisions Windows instances. Use **RSA** or **ECDSA** instead.

To generate a compatible RSA key pair:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_aws_demo -C "your@email.com"
```

Save the **private** key on **APD Machine Credential**. You only need the public key file if running **Create Keypair** standalone without a private key on that credential.


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

**Prerequisites:** AWS credential configured, RSA/ECDSA **private** key on **APD Machine Credential** (same key as RHDP bastion), demo password `Admin_1234!` on that credential for Windows.

### Destroy Cloud Stack in AWS

Use this workflow to completely tear down a stack created by **Deploy Cloud Stack in AWS** and start fresh. Launch it and select the **same AWS Region** used for deploy — that is the only survey prompt.

The workflow:

1. Terminates all five stack VMs **in parallel** (`aws-dc`, `aws_win1`, `aws_rhel8`, `aws_rhel9`, `reports`)
2. Deletes VPC `aws-test-vpc` and related resources (subnet, route table, internet gateway, security group)
3. Deletes keypair `aws-test-key` (runs in parallel with VPC teardown)
4. Syncs AWS inventory so hosts are removed from AAP

**Note:** S3 report buckets created during deploy (`reports-pd-*`) are not deleted by this workflow.

### Other jobs

**Cloud / Create VM** - The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM [blueprints](blueprints/) define variables for each provider that override the defaults in the collection. When creating VMs it is recommended to follow naming conventions that can be used as host patterns. (eg. VM names: `win1`, `win2`, `win3`.  Host Pattern: `win*` )

**Cloud / AWS / Patch EC2 Workflow** - Create a VPC and one or more linux VM(s) in AWS using the `Cloud / Create VPC` and `Cloud / Create VM` templates. Run the workflow and observe the instance snapshots followed by patching operation. Optionally, use the survey to force a patch failure in order to demonstrate the restore path. At this time, the workflow does not support patching Windows instances.

**Cloud / AWS / Resize EC2** - Given an EC2 instance, change its size. This takes an AWS region, target host pattern, and a target instance size as parameters. As a final step, this job refreshes the AWS inventory so the re-created instance is accessible from AAP.

## Known Issues

- **ED25519 key pairs are not supported with Windows AMIs on AWS.** The Deploy Cloud Stack workflow and any job that provisions Windows instances will fail if you register an `ssh-ed25519` public key. Use RSA (`ssh-rsa`) or ECDSA instead.
- Azure does not work without a custom execution environment that includes the Azure dependencies.
