# Cloud Demos

## Table of Contents
- [Cloud Demos](#cloud-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
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

For **Deploy Cloud Stack in AWS**, also add the **private SSH key** (RSA or ECDSA, not ED25519) that pairs with the key registered in AWS. The Create Keypair job derives the public key from this credential automatically — you no longer paste a public key in the workflow survey.

Linux jobs such as **Linux | Fact Scan** will fail with `Permission denied (publickey)` until the matching private key is saved on this credential.

Override the defaults at install time with extra vars if needed:

- `apd_machine_credential_user`
- `apd_machine_credential_password` or `vault_apd_machine_credential_password`

### Getting your Public Key for Create Keypair Job

When launching **Deploy Cloud Stack in AWS** or **Cloud / AWS / Create Keypair**, paste the full public key line into the survey (including any trailing `=` padding and the comment at the end, if present).

**Important:** Do not use **ED25519** keys (`ssh-ed25519`). AWS does not support ED25519 key pairs with Windows AMIs, and the Deploy Cloud Stack workflow provisions Windows instances. Use **RSA** or **ECDSA** instead.

To generate a compatible RSA key:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_aws_demo -C "your@email.com"
cat ~/.ssh/id_rsa_aws_demo.pub
```

Paste the entire output of `cat` into the **Keypair Public Key** survey field.

If you already have a Linux node in AWS from a prior demo run, you can also retrieve a key from that host:

1) Connect to the command line of your Controller server. This is easiest to do by opening the VS Code Web Editor from the landing page where you found the Controller login details.
2) Open a Terminal Window in the VS Code Web Editor.
3) SSH to one of your linux nodes (eg. `ssh aws_rhel9`). This should log you into the node as `ec2-user`
4) `cat .ssh/authorized_keys` and copy the key listed including the `ssh-rsa` prefix


## Suggested Usage

**Deploy Cloud Stack in AWS** - This workflow builds out many helpful and convient resources in AWS. Select an AWS region and it builds a default VPC, keypair (using the SSH private key from **APD Machine Credential**), five VMs (three RHEL and two Windows), and a cloud stats report. VM names, owner tags, and environment values are preset for the demo stack. Use an RSA or ECDSA private key on **APD Machine Credential** — ED25519 keys will fail when Windows instances are provisioned.

**Destroy Cloud Stack in AWS** - Select the same AWS region to tear down the demo stack: terminate all five stack VMs in parallel, delete the VPC, delete the keypair, and refresh inventory. Use this to nuke the stack and start over.

**Cloud / Create VM** - The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM [blueprints](blueprints/) define variables for each provider that override the defaults in the collection. When creating VMs it is recommended to follow naming conventions that can be used as host patterns. (eg. VM names: `win1`, `win2`, `win3`.  Host Pattern: `win*` )

**Cloud / AWS / Patch EC2 Workflow** - Create a VPC and one or more linux VM(s) in AWS using the `Cloud / Create VPC` and `Cloud / Create VM` templates. Run the workflow and observe the instance snapshots followed by patching operation. Optionally, use the survey to force a patch failure in order to demonstrate the restore path. At this time, the workflow does not support patching Windows instances.

**Cloud / AWS / Resize EC2** - Given an EC2 instance, change its size. This takes an AWS region, target host pattern, and a target instance size as parameters. As a final step, this job refreshes the AWS inventory so the re-created instance is accessible from AAP.

## Known Issues

- **ED25519 key pairs are not supported with Windows AMIs on AWS.** The Deploy Cloud Stack workflow and any job that provisions Windows instances will fail if you register an `ssh-ed25519` public key. Use RSA (`ssh-rsa`) or ECDSA instead.
- Azure does not work without a custom execution environment that includes the Azure dependencies.
