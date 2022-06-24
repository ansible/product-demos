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
    - [Getting your Puiblic Key for Create Infra Job](#getting-your-puiblic-key-for-create-infra-job)
  - [Suggested Usage](#suggested-usage)
  - [Known Issues](#known-issues)

## About These Demos
This category of demos shows examples of multi-cloud provisioning and management with Ansible Automation Platform. The list of demos can be found below. These demos are particularly helpful in building additional infrastructure for other demo categories such as Linux and Windows. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Jobs

- [**Cloud / Create Infra**](create_infra.yml) - Creates a VPC with required routing and firewall rules for provisioning VMs
- [**Cloud / Create VM**](create_vm.yml) - Create a VM based on a [blueprint](blueprints/) in the selected cloud provider
- [**Cloud / Destroy VM**](destroy_vm.yml) - Destroy a VM that has been created in a cloud provider. VM must be imported into dynamic inventory to be deleted.

### Inventory

A dynamic inventory is created to pull inventory hosts from cloud providers. The VM will be added by name therefore provisioning VMs with the same name will cause conflict in the inventory.

Groups will be created based on the operating system (platform) of the VM provisioned as well as a group called `cloud_<cloud provider>`.

## Post Setup Setup
After running the setup job template, there are a few steps required to make the demos fully functional. See post setup actions below.

   > These steps may differ if you in your environment

### Configure Credentials

- Add AWS Access and Secret key to the `AWS` Credential created by the setup job.

### Add Workshop Credential Password

1) Add the password used to login to Controller. This allows you to connect to Windows Servers provisioned with Create VM job. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Remove Inventory Variables

1) Remove Workshop Inventory variables on the Details page of the inventory. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Getting your Puiblic Key for Create Infra Job

1) Connect to the command line of your Controller server. This is easiest to do by opening the VS Code Web Editor from the landing page where you found the Controller login details.
2) Open a Terminal Window in the VS Code Web Editor.
3) SSH to one of your linux nodes (eg. `ssh node1`). This should log you into the node as `ec2-user`
4) `cat .ssh/authorized_keys` and copy the key listed including the  `ssh-rsa` prefix


## Suggested Usage

**Cloud / Create Infra** -The Create Infra job builds cloud infrastructure based on the provider definition in the included `demo.cloud` collection.

**Cloud / Create VM** - The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM [blueprints](blueprints/) define variables for each provider that override the defaults in the collection. When creating VMs it is recommended to follow naming conventions that can be used as host patterns. (eg. VM names: `win1`, `win2`, `win3`.  Host Pattern: `win*` )

## Known Issues
Azure does not work without a custom execution environment that includes the Azure dependencies.