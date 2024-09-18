# OpenShift Demos

## Table of Contents
- [OpenShift Demos](#openshift-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of OpenShift operations and management with Ansible Automation Platform. The list of demos can be found below. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Jobs
- [**OpenShift / Dev Spaces**](devspaces.yml) - Install and deploy dev spaces on OCP cluster. After this job has run successfully, login to your OCP cluster, click the application icon (to the left of the bell icon in the top right) to access Dev Spaces
- [**OpenShift / GitLab**](gitlab.yml) - Install and deploy GitLab on OCP.
- [**OpenShift / EDA / Install Controller**](eda/install.yml) - Install and deploy EDA Controller instance using the AAP OpenShift operator.
- **OpenShift / CNV /  Deploy Automation Hub and sync EEs and Collections** - Workflow Job Template to deploy a functional Automaiton Hub instance in OCP.
    - [**OpenShift / Hub / Install Automation Hub**](hub/install.yml) - Install and deploy Automation Hub instance using the AAP OpenShift operator.
    - [**OpenShift / Hub / Sync EE Registries**](hub/registries.yml) - Synchronize Execution Environments from console.redhat.com.
    - [**OpenShift / Hub / Sync Collection Repositories**](hub/collections.yml) - Synchronize collections from console.redhat.com.
- [**OpenShift / CNV / Install Operator**](cnv/install.yml) - Install the Container Native Virtualization (CNV) operator and all its required dependencies.
- **OpenShift / CNV / Infra Stack** - Workflow Job Template to build out infrastructure necessary to run jobs against VMs in OpenShift Virtualization.
    - [**OpenShift / CNV / Create RHEL VM**](cnv/install.yml) - Install the Container Native Virtualization (CNV) operator and all its required dependencies.
- **OpenShift / CNV / Patch CNV Workflow** - Workflow Job Template to snapshot and patch VMs deployed in OpenShift Virtualization.
    - [**OpenShift / CNV / Create VM Snapshots**](cnv/snapshot.yml) - Create snapshot of VMs running in CNV.
    - [**OpenShift / CNV / Patch**](cnv/patch.yml) - Patch VMs in OpenShift CNV, when run in `run` mode build out container native patching report and display link to the user.
    - [**OpenShift / CNV / Restore Latest VM Snapshots**](cnv/snapshot.yml) - Restore VM in CNV to last snapshot.
- [**OpenShift / CNV / Delete VM**](cnv/install.yml) - Deletes VMs in OpenShift CNV.

## Pre Setup
These demos require an OpenShift cluster to deploy to. Luckily the default Ansible Product Demos item from [demo.redhat.com](https://demo.redhat.com) includes an OpenShift cluster. Most of the jobs require an `OpenShift or Kubernetes API Bearer Token` credential in order to interact with OpenShift. When ordered from RHDP this credential is configured for the user.

## Suggested Usage
**OpenShift / EDA / Install Controller** - This job uses the `admin` Controller user's password to configure the EDA controller login of the same name. This job displays the created route after finished and takes roughly 2.5 minutes to run.

**OpenShift / CNV /  Deploy Automation Hub and sync EEs and Collections** - A custom credential type is created for the use in this WJT, `Usable Hub Credential` and it must be filled out in order to pull content from console.redhat.com. This workflow takes roughly 30 minutes to run. This workflow includes the following Job Templates:
- **OpenShift / Hub / Install Automation Hub** - This job does not require a hub credential

- **OpenShift / Hub / Sync EE Registries** - The registries can be configured via `extra_vars` and conforms roughly to those described in [infra.ah_configuration.ah_ee_registry](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/ah_configuration/content/module/ah_ee_registry/).

- **OpenShift / Hub / Sync Collection Repositories** - The collections can be configured via `extra_vars` and conforms roughly to those described in [infra.ah_configuration.collection_repository_sync](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/ah_configuration/content/role/collection_repository_sync/).

**OpenShift / CNV / Install Operator** - This job takes no parameters, to ensure the CNV operator is fully operational it provisions a VM in CNV which is cleaned up upon success.

**OpenShift / CNV / Infra Stack** - This workflow takes three parameters, SSH public key, RHEL activation key, and org ID. The SSH public key is placed as an SSH authorized key, thus in order to then authenticate to these VMs the `Machine Credential` `Demo Credential` must be configured with the private key pair associated with the SSH public key. The RHEL activation key and ID are to receive updates from the DNF repositories for the final patching job. This workflow includes the following Job Templates:
- **OpenShift / CNV / Create RHEL VM** - creates a VM using OpenShift Virtualization
**OpenShift / CNV / Patch CNV Workflow** - This workflow takes an ansible host string as a parameter, by default the hosts generated by APD in CNV are of the format `<namespace>-<vm name>`, for example `openshift-cnv-rhel9`. This workflow includes the following Job Templates:

- **OpenShift / CNV / Create VM Snapshots** - Creates snapshots of VMs relevant to the workflow
- **OpenShift / CNV / Patch** - Patches relevant VMs and generate patching report
- **OpenShift / CNV / Restore Latest VM Snapshots** - restores VMs to their latest snapshot, for the workflow this is invoked upon failure of the patching job. The same host string is used by this job template as the others in the workflow.

**OpenShift / CNV / Delete VM** - Delete VMs based on host string pattern, similar to the other CNV jobs.
