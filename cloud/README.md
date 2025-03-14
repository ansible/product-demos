# Cloud Demos

## Table of Contents
- [Cloud Demos](#cloud-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
    - [Inventory](#inventory)
  - [Post Setup Setup](#post-setup-setup)
    - [Configure Credentials](#configure-credentials)
    - [Add Workshop Credential Password](#add-workshop-credential-password)
    - [Remove Inventory Variables](#remove-inventory-variables)
    - [Getting your Public Key for Create Keypair Job](#getting-your-public-key-for-create-keypair-job)
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

### Add Workshop Credential Password

1) Add a password that meets the [default complexity requirements](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements#reference). This allows you to connect to Windows Servers provisioned with Create VM job. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Remove Inventory Variables

1) Remove Workshop Inventory variables on the Details page of the inventory. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Getting your Public Key for Create Keypair Job

1) Connect to the command line of your Controller server. This is easiest to do by opening the VS Code Web Editor from the landing page where you found the Controller login details.
2) Open a Terminal Window in the VS Code Web Editor.
3) SSH to one of your linux nodes (eg. `ssh aws_rhel9`). This should log you into the node as `ec2-user`
4) `cat .ssh/authorized_keys` and copy the key listed including the  `ssh-rsa` prefix


## Suggested Usage

**Deploy Cloud Stack in AWS** - This workflow builds out many helpful and convient resources in AWS. Given an AWS region, key, and some organizational paremetres for tagging it builds a default VPC, keypair, five VMs (three RHEL and two Windows), and even provides a report for cloud stats. It is the typical starting point for using Ansible Product-Demos in AWS.

**Cloud / Create VM** - The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM [blueprints](blueprints/) define variables for each provider that override the defaults in the collection. When creating VMs it is recommended to follow naming conventions that can be used as host patterns. (eg. VM names: `win1`, `win2`, `win3`.  Host Pattern: `win*` )

**Cloud / AWS / Patch EC2 Workflow** - Create a VPC and one or more linux VM(s) in AWS using the `Cloud / Create VPC` and `Cloud / Create VM` templates. Run the workflow and observe the instance snapshots followed by patching operation. Optionally, use the survey to force a patch failure in order to demonstrate the restore path. At this time, the workflow does not support patching Windows instances.

**Cloud / AWS / Resize EC2** - Given an EC2 instance, change its size. This takes an AWS region, target host pattern, and a target instance size as parameters. As a final step, this job refreshes the AWS inventory so the re-created instance is accessible from AAP.

## Known Issues
Azure does not work without a custom execution environment that includes the Azure dependencies.
